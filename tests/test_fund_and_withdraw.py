from scripts.helpful_scripts import (
    get_account,
    mocks_deploy,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from brownie import FundMe, MockV3Aggregator, accounts, config, network, exceptions
import pytest

account = get_account()


# from scripts.deploy import deploy


def test():
    print(f"we are using a {network.show_active()} network")
    assert network.show_active() == "mainnet-fork-dev"


def test_fund_and_withdraw():

    mocks_deploy()
    price_feed_address = MockV3Aggregator[-1].address
    account = get_account()

    Fund_Me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    entranceFee = Fund_Me.getEntranceFee() + 100
    tx = Fund_Me.fund({"from": account, "value": entranceFee})
    tx.wait(1)
    assert Fund_Me.addressToAmountFunded(account.address) == entranceFee
    tx2 = Fund_Me.withdraw({"from": account})
    tx2.wait(1)
    assert Fund_Me.addressToAmountFunded(account.address) == 0


def test_only_owner():
    if network.show_active() == "mainnet-fork-dev":
        pytest.skip("only for local testing")
    else:
        print("yeah, this is a dev local chain")
    mocks_deploy()
    price_feed_address = MockV3Aggregator[-1].address
    Fund_Me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    thief = accounts.add()
    # Fund_Me.withdraw({"from": accounts.add(config["wallets"]["from_key_02"])})
    with pytest.raises(exceptions.VirtualMachineError):
        Fund_Me.withdraw({"from": accounts.add(config["wallets"]["from_key_02"])})
