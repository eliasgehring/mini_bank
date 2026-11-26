import sqlite3
from typing import Optional

from domains.models import Customer, Account


def insert_customer(
    conn: sqlite3.Connection,
    customer: Customer,
) -> None:
    conn.execute(
        """
        INSERT INTO customers (customer_id, name)
        VALUES (?, ?)
        """,
        (customer.customer_id, customer.name),
    )


def insert_account(
    conn: sqlite3.Connection,
    account: Account,
) -> None:
    conn.execute(
        """
      INSERT INTO accounts (account_id, customer_id)
      VALUES (?,?)
      """,
        (account.account_id, account.customer_id),
    )


def get_customer(
    conn: sqlite3.Connection,
    customer_id: str,
) -> Optional[Customer]:

    row = conn.execute(
        """
    SELECT customer_id, name
    FROM customers
    WHERE customer_id = ?
    """,
        (customer_id,),
    ).fetchone()

    if row is None:
        return None
    return Customer(
        customer_id=row[0],
        name=row[1],
    )


def get_account(
    conn: sqlite3.Connection,
    account_id: str,
) -> Optional[Account]:

    row = conn.execute(
        """
       SELECT account_id, customer_id
       FROM accounts
       WHERE account_id = ?
       """,
        (account_id,),
    ).fetchone()

    if row is None:
        return None
    return Account(
        account_id=row[0],
        customer_id=row[1],
    )
