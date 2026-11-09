from bank_state import accounts, customers, deposits, withdrawals, transfers
from domains.models import Customer, Account, Deposit, Withdrawal
from domains.invariants import validate_deposit, validate_withdrawal, validate_timestamp, validate_amount
from services.balances import compute_balance

def find_customer_accounts(customer_id):
    result=[]
    for account in accounts.values():
        if account.customer_id==customer_id:
            result.append(account)
    return result

def create_customer(customer_id, name):
    if not isinstance(customer_id, str) or not customer_id.strip():
        raise ValueError("Customer ID must be a nonempty string")
    if customer_id in customers:
       raise ValueError("customer_id must not be taken")
    customer=Customer(customer_id=customer_id, name=name)
    customers[customer_id]=customer
    return customer

def open_account(account_id, customer_id):
    if not isinstance(account_id, str) or not account_id.strip():
        raise ValueError("Account ID must be a nonempty string")
    if account_id in accounts:
        raise ValueError("account_id must not be taken")
    if not customer_id in customers:
        raise ValueError("customer must exist")
    account=Account(account_id=account_id, customer_id=customer_id)
    accounts[account_id]=account
    return account 

def make_deposit(id, account_id, amount, timestamp):
    if not account_id in accounts:
        raise ValueError("Account must exist")

    for deposit in deposits:
        if deposit.deposit_id==id:
            raise ValueError("Deposit id must not be taken")
    
    deposit=Deposit(deposit_id=id, account_id=account_id, amount=amount, timestamp=timestamp)
    validate_deposit(deposit)
    validate_timestamp(account_id,timestamp)
    deposits.append(deposit)
    return deposit 

def make_withdrawal(id, account_id, amount, timestamp):
    if not account_id in accounts:
        raise ValueError("Account must exist")
    for withdrawal in withdrawals:
        if withdrawal.withdrawal_id==id:
            raise ValueError("Withdrawal_Id must not be taken")
    withdrawal=Withdrawal(withdrawal_id=id, account_id=account_id, amount=amount, timestamp=timestamp)
    validate_timestamp(account_id,timestamp)
    validate_withdrawal(withdrawal)
    current_balance= compute_balance(account_id,deposits, withdrawals, transfers)
    if current_balance<amount:
        raise ValueError("Insufficient funds")
  
    withdrawals.append(withdrawal)
    return withdrawal




