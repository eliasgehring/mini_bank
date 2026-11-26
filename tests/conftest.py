import pytest

from bank_state import (
    customers,
    accounts,
    deposits,
    withdrawals,
    transfers,
)


@pytest.fixture(autouse=True)
def clean_bank_state():
    customers.clear()
    accounts.clear()
    deposits.clear()
    withdrawals.clear()
    transfers.clear()
