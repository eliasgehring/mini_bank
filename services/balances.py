from decimal import Decimal
def compute_balance(account_id, deposits, withdrawals, transfers):
    balance = Decimal("0.00")
    for deposit in deposits:
        if deposit.account_id==account_id:
            balance= balance+ deposit.amount
    for withdrawal in withdrawals:
        if withdrawal.account_id==account_id:
            balance= balance- withdrawal.amount 
    for transfer in transfers:
        if transfer.sender_account_id==account_id:
            balance= balance-transfer.amount
        if transfer.receiver_account_id==account_id:
            balance= balance+ transfer.amount
    return balance
