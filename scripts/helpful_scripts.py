from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]
DECIMALS = 8
STARTING_VALUE = 200000000000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "localnew", "None", "mainnet-fork-dev"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key_02"])
        


def mocks_deploy():
    MockV3Aggregator.deploy(
        DECIMALS,
        STARTING_VALUE,
        {"from": get_account()},
    )
    print("mockV3Aggregator deployed")
