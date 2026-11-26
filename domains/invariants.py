from domains.models import Transfer, Deposit, Withdrawal
from bank_state import deposits, withdrawals, transfers
from decimal import Decimal

from datetime import datetime

MAX_TRANSACTION_AMOUNT = Decimal("999999999999.99")


def validate_transfer(transfer: Transfer) -> None:
    validate_amount(transfer.amount)
    if not isinstance(transfer.transfer_id, str) or not transfer.transfer_id.strip():
        raise ValueError("Transfer Id must not be empty")
    if transfer.sender_account_id == transfer.receiver_account_id:
        raise ValueError("Self transfer is not permitted")


def validate_deposit(deposit: Deposit) -> None:
    validate_amount(deposit.amount)
    if not isinstance(deposit.deposit_id, str) or not deposit.deposit_id.strip():
        raise ValueError("Deposit Id must not be empty")


def validate_withdrawal(withdrawal: Withdrawal) -> None:
    validate_amount(withdrawal.amount)
    if (
        not isinstance(withdrawal.withdrawal_id, str)
        or not withdrawal.withdrawal_id.strip()
    ):
        raise ValueError("Withdrawal Id must not be empty")


def latest_timestamp_for_account(account_id):
    latest = None
    for deposit in deposits:
        if deposit.account_id == account_id:
            if latest is None or deposit.timestamp > latest:
                latest = deposit.timestamp
    for withdrawal in withdrawals:
        if withdrawal.account_id == account_id:
            if latest is None or withdrawal.timestamp > latest:
                latest = withdrawal.timestamp
    for transfer in transfers:
        if (
            transfer.sender_account_id == account_id
            or transfer.receiver_account_id == account_id
        ):
            if latest is None or transfer.timestamp > latest:
                latest = transfer.timestamp
    return latest


def validate_timestamp(account_id, timestamp):
    if isinstance(timestamp, datetime) == False:
        raise ValueError("Timestamp must be a datetime")
    latest = latest_timestamp_for_account(account_id)
    if latest is None:
        return
    latest_is_naive = latest.utcoffset() is None
    new_is_naive = timestamp.utcoffset() is None
    if latest_is_naive != new_is_naive:
        raise ValueError("Timezones must be of same type")
    if latest is None:
        return
    if latest > timestamp:
        raise ValueError("Event must not precede account history")


def validate_amount(amount):
    if not isinstance(amount, Decimal):
        raise ValueError("Amount must be a decimal")
    if amount.is_finite() == False:
        raise ValueError("Amount must be finite")
    if amount <= Decimal("0.00"):
        raise ValueError("Amount must be positive")

    if amount > MAX_TRANSACTION_AMOUNT:
        raise ValueError("Amount exceeds maximum transaction amount")
    if amount != amount.quantize(Decimal("0.01")):
        raise ValueError("Amount must be expressed in full cents")
