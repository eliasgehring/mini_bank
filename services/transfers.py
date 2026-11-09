from domains.models import Transfer
from bank_state import transfers, accounts, deposits, withdrawals
from services.balances import compute_balance
from domains.invariants import validate_transfer, validate_timestamp

def make_transfer(id, sender_account_id, receiver_account_id, amount, timestamp):
    if sender_account_id not in accounts or receiver_account_id not in accounts:
        raise ValueError("Both accounts must exist")
    for transfer in transfers:
        if transfer.transfer_id==id:
            raise ValueError("Transfer ID already exists")
    transfer= Transfer(transfer_id=id, sender_account_id=sender_account_id, receiver_account_id=receiver_account_id, amount=amount, timestamp=timestamp)
    validate_transfer(transfer)
    validate_timestamp(sender_account_id,timestamp)
    validate_timestamp(receiver_account_id,timestamp)
    current_balance= compute_balance(sender_account_id, deposits, withdrawals,transfers)
    if amount>current_balance:
        raise ValueError("Insufficient funds")
    transfers.append(transfer)
    return transfer

