from pyband import Client

def main():
    # Step 1
    test_net = "laozi-testnet4.bandchain.org/grpc-web"
    grpc_url = test_net # ex.laozi-testnet4.bandchain.org(without https://)
    c = Client(grpc_url)

    # Step 2
    print(c.get_reference_data(["BTC/USD", "ETH/USD"], 3, 4))

if __name__ == "__main__":
    main()