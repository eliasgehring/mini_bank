from decimal import Decimal
from domains.models import Deposit, Withdrawal
from datetime import datetime
from services.balances import compute_balance


def test_single_deposit_gives_100():
    deposit = Deposit(
        deposit_id="deposit_1",
        account_id="alice_account",
        amount=Decimal("100.00"),
        timestamp=datetime(2026, 9, 10, 12, 0),
    )
    assert compute_balance("alice_account", [deposit], [], []) == Decimal("100.00")


def test_withdrawal_gives_70():
    deposit = Deposit(
        deposit_id="deposit_1",
        account_id="alice_account",
        amount=Decimal("100.00"),
        timestamp=datetime(2026, 9, 10, 12, 0),
    )
    withdrawal = Withdrawal(
        withdrawal_id="withdrawal_1",
        account_id="alice_account",
        amount=Decimal("30.00"),
        timestamp=datetime(2026, 9, 10, 13, 0),
    )
    assert compute_balance("alice_account", [deposit], [withdrawal], []) == Decimal(
        "70.00"
    )


def test_alice_bob():
    alice_deposit = Deposit(
        deposit_id="deposit_1",
        account_id="alice_account",
        amount=Decimal("100.00"),
        timestamp=datetime(2026, 12, 12, 12),
    )
    bob_deposit = Deposit(
        deposit_id="deposit_2",
        account_id="bob_account",
        amount=Decimal("100.00"),
        timestamp=datetime(2026, 12, 12, 12),
    )
    withdrawal = Withdrawal(
        withdrawal_id="Withdrawal_1",
        account_id="bob_account",
        amount=Decimal("50"),
        timestamp=datetime(2026, 12, 12, 12),
    )
    assert compute_balance(
        "alice_account", [alice_deposit], [withdrawal], []
    ) == Decimal("100.00")
