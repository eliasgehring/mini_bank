from services.accounts import (
    open_account,
    make_deposit,
    create_customer,
    make_withdrawal,
)
from services.transfers import make_transfer
from bank_state import deposits, withdrawals, transfers, customers, accounts
from decimal import Decimal
from datetime import datetime
import pytest
from domains.invariants import validate_amount


def clear_state():
    customers.clear()
    accounts.clear()
    deposits.clear()
    withdrawals.clear()
    transfers.clear()


def test_infinite_amount_gets_rejected():
    amount = Decimal("Infinity")
    with pytest.raises(ValueError):
        validate_amount(amount)
    amount = Decimal("0.001")
    with pytest.raises(ValueError):
        validate_amount(amount)
    amount = Decimal("NaN")
    with pytest.raises(ValueError):
        validate_amount(amount)
    amount = 12.3
    with pytest.raises(ValueError):
        validate_amount(amount)


def test_extremely_large_amount_rejected():
    with pytest.raises(ValueError):
        validate_amount(Decimal("1e30"))


def test_maximum_transaction_amount_accepted():
    validate_amount(Decimal("999999999999.99"))


def test_self_transfer_rejected():
    clear_state()
    create_customer("Alice_1", "Alice")
    account_alice = open_account("alice_account_1", "Alice_1")
    make_deposit(
        "deposit_1", "alice_account_1", Decimal("100"), datetime(11, 11, 11, 11)
    )
    with pytest.raises(ValueError):
        make_transfer(
            "transfer_1",
            "alice_account_1",
            "alice_account_1",
            Decimal("20"),
            datetime(12, 12, 12, 12),
        )
