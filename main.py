import os

from pyband import Client, Transaction, PrivateKey

from pyband.proto.cosmos.base.v1beta1.coin_pb2 import Coin
from pyband.proto.oracle.v1.tx_pb2 import MsgRequestData
from google.protobuf.json_format import MessageToJson


def main():
    # Step 1 Create a gRPC connection
    grpc_url = "rpc-laozi-testnet2.bandchain.org:9090"
    c = Client(grpc_url, insecure=True)

    # Step 2 Convert a menmonic to private key, public key, and sender
    MNEMONIC = os.getenv("MNEMONIC")
    private_key = PrivateKey.from_mnemonic(MNEMONIC)
    public_key = private_key.to_public_key()
    sender_addr = public_key.to_address()
    sender = sender_addr.to_acc_bech32()

    # Step 3 Prepare a transaction's properties
    request_msg = MsgRequestData(
        oracle_script_id=37,
        calldata=bytes.fromhex("0000000200000003425443000000034554480000000000000064"),
        ask_count=4,
        min_count=3,
        client_id="BandProtocol",
        fee_limit=[Coin(amount="100", denom="uband")],
        prepare_gas=50000,
        execute_gas=200000,
        sender=sender,
    )

    account = c.get_account(sender)
    account_num = account.account_number
    sequence = account.sequence

    fee = [Coin(amount="0", denom="uband")]
    chain_id = c.get_chain_id()

    # Step 4 Construct a transaction
    txn = (
        Transaction()
        .with_messages(request_msg)
        .with_sequence(sequence)
        .with_account_num(account_num)
        .with_chain_id(chain_id)
        .with_gas(2000000)
        .with_fee(fee)
        .with_memo("")
    )

    # Step 5 Sign a transaction by using private key
    sign_doc = txn.get_sign_doc(public_key)
    signature = private_key.sign(sign_doc.SerializeToString())
    tx_raw_bytes = txn.get_tx_data(signature, public_key)

    # Step 6 Broadcast a transaction
    tx_block = c.send_tx_block_mode(tx_raw_bytes)

    # Converting to JSON for readability
    print(MessageToJson(tx_block))


if __name__ == "__main__":
    main()