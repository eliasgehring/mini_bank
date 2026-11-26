import sqlite3
from pathlib import Path


def connect_db(path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_schema(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS accounts (
            account_id TEXT PRIMARY KEY NOT NULL,
            customer_id TEXT NOT NULL,
            FOREIGN KEY (customer_id)
                REFERENCES customers(customer_id)
        )
    """
    )

    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS deposits (
        deposit_id TEXT PRIMARY KEY NOT NULL,
        account_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        timestamp TEXT NOT NULL,

        FOREIGN KEY (account_id)
            REFERENCES accounts(account_id),

        CHECK (amount_cents > 0),
        CHECK (amount_cents <= 99999999999999)
    )
"""
    )

    conn.execute(
        """ CREATE TABLE IF NOT EXISTS withdrawals (
        withdrawal_id TEXT PRIMARY KEY NOT NULL,
        account_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        timestamp TEXT NOT NULL,

        FOREIGN KEY (account_id)
          REFERENCES accounts(account_id),

        CHECK (amount_cents > 0),
        CHECK (amount_cents <= 99999999999999)
    )
"""
    )

    conn.execute(
        """ CREATE TABLE IF NOT EXISTS transfers (
        transfer_id TEXT PRIMARY KEY NOT NULL,
        sender_account_id TEXT NOT NULL, 
        receiver_account_id TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        
        FOREIGN KEY (sender_account_id)
          REFERENCES accounts(account_id),
        
        FOREIGN KEY (receiver_account_id)
          REFERENCES accounts(account_id),
    
        CHECK (amount_cents > 0),
        CHECK (amount_cents <= 99999999999999),
        CHECK (sender_account_id != receiver_account_id)
        )
    """
    )
    conn.commit()


if __name__ == "__main__":
    conn = connect_db("minibank_dev.db")
    initialize_schema(conn)
    conn.close()

    print("Database initialized successfully.")
