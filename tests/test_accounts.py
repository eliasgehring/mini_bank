import pytest 

from services.accounts import create_customer, open_account
from bank_state import customers, accounts

def test_customer_id_uniqueness():
    create_customer("customer_1", "Alice")
    with pytest.raises(ValueError):
        create_customer("customer_1", "Bob")


def test_customer_rejects_empty_id():
    with pytest.raises(ValueError):
        create_customer("", "Alice")
    assert len(customers)==0

def test_account_rejects_empty_id():
    create_customer("Alice_1", "Alice")
    with pytest.raises(ValueError):
        open_account("","Alice_1")
    assert len(accounts)==0