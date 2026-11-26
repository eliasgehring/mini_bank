from services.accounts import (
    open_account,
    make_deposit,
    create_customer,
    make_withdrawal,
)
from services.transfers import make_transfer
from services.balances import compute_balance
from bank_state import deposits, withdrawals, transfers
from decimal import Decimal
from datetime import datetime
from domains.models import Transfer
import pytest


def test_transfer_integration():
    create_customer("customer_1", "Alice")
    create_customer("customer_2", "Bob")
    alice_account = open_account("alice_account_1", "customer_1")
    bob_account = open_account("bob_account_1", "customer_2")
    make_deposit(
        "deposit_1",
        alice_account.account_id,
        Decimal("100.00"),
        datetime(2026, 12, 12, 12),
    )
    result = make_transfer(
        "transfer_1",
        alice_account.account_id,
        bob_account.account_id,
        Decimal("30.00"),
        datetime(2026, 12, 12, 13),
    )
    alice_balance = compute_balance(
        alice_account.account_id, deposits, withdrawals, transfers
    )
    bob_balance = compute_balance(
        bob_account.account_id, deposits, withdrawals, transfers
    )

    assert alice_balance == Decimal("70.00")
    assert bob_balance == Decimal("30.00")
    assert alice_balance + bob_balance == Decimal("100.00")
    assert len(transfers) == 1
    assert len(deposits) == 1
    assert isinstance(result, Transfer)
    assert result.transfer_id == "transfer_1"


def test_transfer_id_uniqueness():
    create_customer("customer_1", "Alice")
    create_customer("customer_2", "Bob")
    alice_account = open_account("alice_account_1", "customer_1")
    bob_account = open_account("bob_account_1", "customer_2")
    make_deposit(
        "deposit_1",
        alice_account.account_id,
        Decimal("30.00"),
        datetime(2026, 11, 11, 11),
    )
    make_transfer(
        "transfer_1",
        alice_account.account_id,
        bob_account.account_id,
        Decimal("20.00"),
        datetime(2026, 12, 12, 12),
    )
    with pytest.raises(ValueError):
        make_transfer(
            "transfer_1",
            alice_account.account_id,
            bob_account.account_id,
            Decimal("5.00"),
            datetime(2026, 12, 13, 13),
        )


def test_deposit_id_uniqueness():
    create_customer("customer_1", "Alice")
    alice_account = open_account("alice_account_1", "customer_1")
    make_deposit(
        "deposit_1",
        alice_account.account_id,
        Decimal("30.00"),
        datetime(2026, 12, 12, 12),
    )
    with pytest.raises(ValueError):
        make_deposit(
            "deposit_1",
            alice_account.account_id,
            Decimal("20.00"),
            datetime(2026, 12, 13, 13),
        )


def test_withdrawal_id_uniqueness():
    create_customer("customer_1", "Alice")
    alice_account = open_account("alice_account_1", "customer_1")
    make_deposit(
        "deposit_1",
        alice_account.account_id,
        Decimal("100.00"),
        datetime(2026, 12, 12, 12),
    )
    make_withdrawal(
        "withdrawal_1",
        alice_account.account_id,
        Decimal("20.00"),
        datetime(2026, 12, 13, 13),
    )
    with pytest.raises(ValueError):
        make_withdrawal(
            "withdrawal_1",
            alice_account.account_id,
            Decimal("30.00"),
            datetime(2026, 12, 14, 14),
        )


def test_multi_account_conservation():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    create_customer("Charlie_1", "Charlie")
    alice_account = open_account("alice_account_1", "Alice_1")
    bob_account = open_account("bob_account_1", "Bob_1")
    charlie_account = open_account("charlie_account_1", "Charlie_1")
    make_deposit(
        "deposit_1", "alice_account_1", Decimal("100"), datetime(2026, 1, 1, 12)
    )
    make_deposit("deposit_2", "bob_account_1", Decimal("40"), datetime(2026, 1, 2, 1))
    make_transfer(
        "transfer_1",
        "alice_account_1",
        "bob_account_1",
        Decimal("30"),
        datetime(2026, 3, 2, 1),
    )
    make_transfer(
        "transfer_2",
        "bob_account_1",
        "charlie_account_1",
        Decimal("20"),
        datetime(2026, 4, 3, 2),
    )
    make_transfer(
        "transfer_3",
        "charlie_account_1",
        "alice_account_1",
        Decimal("5"),
        datetime(2026, 5, 4, 3),
    )
    make_withdrawal(
        "withdrawal_1", "alice_account_1", Decimal("10"), datetime(2026, 6, 1, 1)
    )
    alice_final_cash = compute_balance(
        "alice_account_1", deposits, withdrawals, transfers
    )
    bob_final_cash = compute_balance("bob_account_1", deposits, withdrawals, transfers)
    charlie_final_cash = compute_balance(
        "charlie_account_1", deposits, withdrawals, transfers
    )

    assert alice_final_cash == Decimal("65")
    assert bob_final_cash == Decimal("50")
    assert charlie_final_cash == Decimal("15")

    assert len(deposits) == 2
    assert len(transfers) == 3
    assert len(withdrawals) == 1


def test_withdrawal_cannot_overspend_after_transfer():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    alice_account = open_account("alice_account_1", "Alice_1")
    bob_account = open_account("bob_account_1", "Bob_1")
    make_deposit(
        "deposit_1", "alice_account_1", Decimal("100"), datetime(2026, 1, 1, 12)
    )
    make_transfer(
        "transfer_1",
        "alice_account_1",
        "bob_account_1",
        Decimal("80"),
        datetime(2026, 3, 2, 1),
    )
    with pytest.raises(ValueError):
        make_withdrawal(
            "withdrawal_1", "alice_account_1", Decimal("30"), datetime(2026, 6, 1, 1)
        )
    make_withdrawal(
        "withdrawal_1", "alice_account_1", Decimal("20"), datetime(2026, 6, 1, 1)
    )
    alice_final_cash = compute_balance(
        "alice_account_1", deposits, withdrawals, transfers
    )
    bob_final_cash = compute_balance("bob_account_1", deposits, withdrawals, transfers)

    assert alice_final_cash == Decimal("0.00")
    assert bob_final_cash == Decimal("80")
    assert len(deposits) == 1
    assert len(transfers) == 1
    assert len(withdrawals) == 1


def test_balance_queries_are_order_independent():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    open_account("alice_account", "Alice_1")
    open_account("bob_account", "Bob_1")
    make_deposit(
        "deposit_1",
        "alice_account",
        Decimal("100.00"),
        datetime(2026, 11, 1, 10, 0),
    )
    make_deposit(
        "deposit_2",
        "bob_account",
        Decimal("20.00"),
        datetime(2026, 11, 1, 10, 1),
    )
    make_transfer(
        "transfer_1",
        "alice_account",
        "bob_account",
        Decimal("35.00"),
        datetime(2026, 11, 1, 10, 2),
    )
    make_withdrawal(
        "withdrawal_1",
        "bob_account",
        Decimal("10.00"),
        datetime(2026, 11, 1, 10, 3),
    )
    history_before = (
        tuple(deposits),
        tuple(withdrawals),
        tuple(transfers),
    )
    bob_1 = compute_balance("bob_account", deposits, withdrawals, transfers)
    alice_1 = compute_balance("alice_account", deposits, withdrawals, transfers)
    alice_2 = compute_balance("alice_account", deposits, withdrawals, transfers)
    bob_2 = compute_balance("bob_account", deposits, withdrawals, transfers)

    assert alice_1 == alice_2 == Decimal("65.00")
    assert bob_1 == bob_2 == Decimal("45.00")

    for _ in range(3):
        assert compute_balance(
            "alice_account", deposits, withdrawals, transfers
        ) == Decimal("65.00")

    assert history_before == (
        tuple(deposits),
        tuple(withdrawals),
        tuple(transfers),
    )


def test_deposit_rejected_when_backdated_before_incoming_transfer():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    open_account("alice_account_1", "Alice_1")
    open_account("bob_account_1", "Bob_1")
    make_deposit(
        "deposit_1",
        "alice_account_1",
        Decimal("100.00"),
        datetime(2026, 1, 1, 10, 0),
    )
    make_transfer(
        "transfer_1",
        "alice_account_1",
        "bob_account_1",
        Decimal("40"),
        datetime(2026, 1, 1, 10, 30),
    )
    with pytest.raises(ValueError):
        make_deposit(
            "deposit_2", "bob_account_1", Decimal("10"), datetime(2026, 1, 1, 10, 15)
        )
    alice_cash_after_failed_deposit = compute_balance(
        "alice_account_1", deposits, withdrawals, transfers
    )
    bob_cash_after_failed_deposit = compute_balance(
        "bob_account_1", deposits, withdrawals, transfers
    )

    assert alice_cash_after_failed_deposit == Decimal("60")
    assert bob_cash_after_failed_deposit == Decimal("40")

    make_deposit(
        "deposit_2", "bob_account_1", Decimal("10"), datetime(2026, 1, 1, 10, 31)
    )

    alice_final_cash = compute_balance(
        "alice_account_1", deposits, withdrawals, transfers
    )
    bob_final_cash = compute_balance("bob_account_1", deposits, withdrawals, transfers)

    assert alice_final_cash == 60
    assert bob_final_cash == 50

    assert len(deposits) == 2
    assert len(transfers) == 1


def test_transfer_rejection_is_atomic():
    create_customer("Alice_1", "Alice")
    create_customer("Bob_1", "Bob")
    open_account("alice_account_1", "Alice_1")
    open_account("bob_account_1", "Bob_1")
    make_deposit(
        "deposit_1", "alice_account_1", Decimal("100"), datetime(2026, 1, 1, 10, 0)
    )
    make_deposit(
        "deposit_2", "bob_account_1", Decimal("20"), datetime(2026, 1, 1, 10, 20)
    )
    with pytest.raises(ValueError):
        make_transfer(
            "transfer_1",
            "alice_account_1",
            "bob_account_1",
            Decimal("30"),
            datetime(2026, 1, 1, 10, 10),
        )
    make_transfer(
        "transfer_1",
        "alice_account_1",
        "bob_account_1",
        Decimal("30"),
        datetime(2026, 1, 1, 10, 21),
    )
    alice_final_cash = compute_balance(
        "alice_account_1", deposits, withdrawals, transfers
    )
    bob_final_cash = compute_balance("bob_account_1", deposits, withdrawals, transfers)

    assert alice_final_cash == Decimal("70")
    assert bob_final_cash == Decimal("50")
    assert len(deposits) == 2
    assert len(transfers) == 1


def test_multiple_accounts_same_customer_are_isolated():
    create_customer("Alice_1", "Alice")
    alice_savings_account = open_account("alice_savings_account_1", "Alice_1")
    alice_checking_account = open_account("alice_checking_account_1", "Alice_1")
    make_deposit(
        "deposit_1",
        "alice_savings_account_1",
        Decimal("100"),
        datetime(2026, 1, 1, 10, 0),
    )
    make_deposit(
        "deposit_2",
        "alice_checking_account_1",
        Decimal("20"),
        datetime(2026, 1, 1, 10, 1),
    )
    with pytest.raises(ValueError):
        make_withdrawal(
            "withdrawal_1",
            "alice_checking_account_1",
            Decimal("30"),
            datetime(2026, 1, 1, 10, 2),
        )
    make_transfer(
        "transfer_1",
        "alice_savings_account_1",
        "alice_checking_account_1",
        Decimal("40"),
        datetime(2026, 1, 1, 10, 3),
    )
    make_withdrawal(
        "withdrawal_1",
        "alice_checking_account_1",
        Decimal("30"),
        datetime(2026, 1, 1, 10, 4),
    )

    alice_savings_account_final_cash = compute_balance(
        "alice_savings_account_1", deposits, withdrawals, transfers
    )
    alice_checking_account_final_cash = compute_balance(
        "alice_checking_account_1", deposits, withdrawals, transfers
    )
    alice_final_cash = (
        alice_savings_account_final_cash + alice_checking_account_final_cash
    )

    assert alice_savings_account_final_cash == Decimal("60")
    assert alice_checking_account_final_cash == Decimal("30")
    assert alice_final_cash == Decimal("90")
    assert len(deposits) == 2
    assert len(withdrawals) == 1
    assert len(transfers) == 1
