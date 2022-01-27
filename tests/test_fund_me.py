from brownie import FundMe, network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me

import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntraceFee() + 100
    # first fund
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee
    # now withdraw
    tx1 = fund_me.withdraw({"from": account})
    tx1.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


# to run this test only in development env
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")

    # account = get_account()
    fund_me = deploy_fund_me()
    # generates a random account
    bad_actor_account = accounts.add()
    # This call should fail because withdraw function only allows
    # the owner to withdraw
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor_account})
