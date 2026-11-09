from dataclasses import dataclass 
from decimal import Decimal
from datetime import datetime 

@dataclass(frozen=True)
class Customer:
    customer_id: str
    name: str

@dataclass(frozen=True)
class Account:
    account_id: str
    customer_id: str

@dataclass(frozen=True)
class Transfer:
    transfer_id: str
    sender_account_id: str
    receiver_account_id: str
    amount: Decimal
    timestamp: datetime 


@dataclass(frozen=True)
class Deposit:
    deposit_id: str
    account_id: str
    amount: Decimal 
    timestamp: datetime

@dataclass(frozen=True)
class Withdrawal:
    withdrawal_id: str
    account_id: str
    amount: Decimal 
    timestamp: datetime
    



