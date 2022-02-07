from brownie import FundMe, MockV3Aggregator, accounts, config, network
from scripts.helpful_scripts import (
    get_account,
    mocks_deploy,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# If we are in a persistent network like rinkeby, use associatted address
# otherwise, please use a mock
account = get_account()

print("he seteado el account")
if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
    price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    print(f"I am on {network.show_active()} network")
    print(account)
else:
    print(f"we are using a {network.show_active()} network")
    if len(MockV3Aggregator) == 0:
        mocks_deploy()
        price_feed_address = MockV3Aggregator[-1].address


def deploy():

    Fund_Me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )


def main():
    deploy()
