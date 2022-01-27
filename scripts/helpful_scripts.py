from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3


# To match the code
DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev-2"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print(".....Returning account from development {account[0]}")
        return accounts[0]
    else:
        print("....not sure why we are getting the private key")
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks....")
    # Counts the number of MockV3Aggregator deployed
    if len(MockV3Aggregator) <= 0:
        # MockV3Aggregator.deploy(
        # DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        # )

        # using exact values to match the code in FundMe
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mocks Deployed!")
