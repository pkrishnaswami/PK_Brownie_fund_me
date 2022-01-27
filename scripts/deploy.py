from brownie import FundMe, network, config, MockV3Aggregator

from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our fundme contract
    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        # print(f"The active network is {network.show_active()}")
        # print("Deploying Mocks....")
        # Counts the number of MockV3Aggregator deployed
        # if len(MockV3Aggregator) <= 0:
        # MockV3Aggregator.deploy(18, Web3.toWei(2000, "ether"), {"from": account})
        # print("Mocks Deployed!")
        # deploy the most recently deployed mock_aggregator
        price_feed_address = MockV3Aggregator[-1].address

    print(f" account address {account}")
    print(f"price feed {price_feed_address}")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    # instead just passing in true
    print(f"Contract deployed to {fund_me.address}")
    # can be used by other contracts including tests
    return fund_me


def main():
    deploy_fund_me()
