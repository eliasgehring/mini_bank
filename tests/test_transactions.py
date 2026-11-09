import pytest

from bank_state import deposits, withdrawals, transfers
from services.accounts import create_customer, open_account, make_deposit, make_withdrawal, compute_balance
from services.transfers import make_transfer

from datetime import datetime, timezone, timedelta
from decimal import Decimal

def test_deposit_rejects_empty_id():
    create_customer("Alice_1", "Alice")
    account_alice= open_account("alice_account_1","Alice_1")
    with pytest.raises(ValueError):
        make_deposit("","alice_account_1",Decimal("100"),datetime(11,11,11,11))
    assert len(deposits)==0

def test_withdrawal_rejects_empty_id():
    create_customer("Alice_1", "Alice")
    account_alice= open_account("alice_account_1","Alice_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(11,11,11,11))
    with pytest.raises(ValueError):
        make_withdrawal("","alice_account_1",Decimal("30"),datetime(12,11,11,11))
    assert len(withdrawals)==0

def test_transfer_rejects_empty_id():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1","Bob")
    account_alice= open_account("alice_account_1","Alice_1")
    account_bob= open_account("bob_account_1","Bob_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(11,11,11,11))
    make_deposit("deposit_2","bob_account_1",Decimal("100"),datetime(11,11,11,11))
    with pytest.raises(ValueError):
        make_transfer("","alice_account_1","bob_account_1",Decimal("100"),datetime(11,11,11,12))


def test_withdrawal_cannot_happen_before_existing_deposit():
    create_customer("customer_1","Alice")
    alice_account=open_account("alice_account_1","customer_1")
    make_deposit("deposit_1",alice_account.account_id,Decimal("30.00"),datetime(2026,12,12,12))
    with pytest.raises(ValueError):
        make_withdrawal("withdrawal_1",alice_account.account_id,Decimal("30.00"),datetime(2026,11,12,12))

def test_deposit_rejects_missing_timestamp():
    create_customer("Alice1","Alice")
    alice_account=open_account("alice_account_1","Alice1")
    with pytest.raises(ValueError):
        make_deposit("deposit_1","alice_account_1",Decimal("100.00"),timestamp=None)

def test_mixed_timestamp_types_rejected():
    create_customer("Alice_1", "Alice")
    account_alice= open_account("alice_account_1","Alice_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(11,11,11,11))
    with pytest.raises(ValueError):
        make_withdrawal("withdrawal_1","alice_account_1",Decimal("50"),datetime(12,12,12,12,tzinfo=timezone.utc))


def test_different_aware_timezones_accepted():
    create_customer("Alice_1", "Alice")
    account_alice= open_account("alice_account_1","Alice_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(11,11,11,11,tzinfo=timezone(timedelta(hours=1))))
    make_withdrawal("withdrawal_1","alice_account_1",Decimal("50"),datetime(12,12,12,12,tzinfo=timezone.utc))


def test_transfer_cannot_precede_receiver_history():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    account_alice= open_account("alice_account_1","Alice_1")
    account_bob= open_account("bob_account_1","Bob_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(2025,11,11,12))
    make_deposit("deposit_2","bob_account_1",Decimal("100"),datetime(2025,11,11,15))
    with pytest.raises(ValueError):
        make_transfer("transfer_1","alice_account_1","bob_account_1",Decimal("100"),datetime(2025,11,11,14))

def test_withdrawal_rejected_when_funds_insufficient():
    create_customer("customer_1", "Alice")
    alice_account=open_account("alice_account_1","customer_1")
    make_deposit("deposit_1", alice_account.account_id,Decimal("100.00"),datetime(2026,12,12,12))
    assert len(deposits)==1
    make_withdrawal("withdrawal_1",alice_account.account_id,Decimal("30.00"),datetime(2026,12,12,12))
    with pytest.raises(ValueError):
        make_withdrawal("withdrawal_2",alice_account.account_id, Decimal("120"),datetime(2026,12,12,12))
    alice_balance=compute_balance(alice_account.account_id,deposits,withdrawals,transfers)
    assert len(withdrawals)==1
    assert alice_balance==Decimal("70.00")


def test_transfer_rejected_when_funds_insufficient():
    create_customer("customer_1", "Alice")
    create_customer("customer_2", "Bob")
    alice_account=open_account("alice_account_1","customer_1")
    bob_account=open_account("bob_account_1","customer_2")
    make_deposit("deposit_1", alice_account.account_id,Decimal("100.00"),datetime(2026,12,12,12))
    assert len(deposits)==1
    assert len(transfers)==0
    
    with pytest.raises(ValueError):
        make_transfer("transfer_1",alice_account.account_id, bob_account.account_id, Decimal("120.00"),datetime(2026,12,12,13))
    alice_balance=compute_balance(alice_account.account_id,deposits,withdrawals,transfers)
    bob_balance=compute_balance(bob_account.account_id,deposits,withdrawals,transfers)
    assert len(transfers)==0
    assert alice_balance==Decimal("100.00")
    assert bob_balance==Decimal("0.00")
    assert alice_balance+bob_balance==Decimal("100")


def test_only_valid_money_can_enter():
    create_customer("customer_1","Alice")
    alice_account=open_account("alice_account_1","customer_1")
    with pytest.raises(ValueError):
        make_deposit("deposit_1",alice_account.account_id,Decimal("0.001"), datetime(2026,10,10,10))

    assert len(deposits)==0


def test_nan_withdrawal_rejected_without_mutation():
    create_customer("Alice_1", "Alice")
    account_alice= open_account("alice_account_1","Alice_1")
    make_deposit("deposit_1","alice_account_1",Decimal("100"),datetime(11,11,11,11))
    with pytest.raises(ValueError):
        make_withdrawal("withdrawal_1","alice_account_1",Decimal("NaN"),datetime(12,12,12,12))