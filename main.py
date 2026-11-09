from domains.models import Customer, Account
from bank_state import customers, accounts, deposits, withdrawals, transfers
from services.accounts import create_customer
from services.accounts import open_account, make_deposit, make_withdrawal
from services.transfers import make_transfer
from services.balances import compute_balance
from decimal import Decimal 
from datetime import datetime


def main():
    alice=create_customer("customer_1","Alice")
    bob=create_customer("customer_2", "Bob")
    
    alice_account=open_account("alice_account_1", "customer_1")
    bob_account=open_account("bob_account_1","customer_2")
    make_deposit("deposit_1",alice_account.account_id, Decimal("100.00"), datetime(2026,11, 12, 12) )
    make_transfer("transfer_1",alice_account.account_id,bob_account.account_id,Decimal("30"), datetime(2026,12,12,12))
    alice_balance=compute_balance(alice_account.account_id, deposits, withdrawals, transfers)
    bob_balance=compute_balance(bob_account.account_id, deposits, withdrawals, transfers)
    print(alice_balance)
    print(bob_balance)
    print(alice_balance+bob_balance)

if __name__=="__main__":
    main()

