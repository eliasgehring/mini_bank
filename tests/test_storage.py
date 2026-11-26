import sqlite3
from storage.database import connect_db, initialize_schema
from domains.models import Customer, Account
from storage.sqlite_repository import (
    insert_customer,
    get_customer,
    insert_account,
    get_account,
)
import pytest


def test_customer_survives_reopen(tmp_path):
    db_path = tmp_path / "test_bank_db"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    customer = Customer("customer_1", "alice")
    insert_customer(conn, customer)
    conn.commit()
    conn.close()
    db_path = tmp_path / "test_bank_db"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    get_customer(conn, "customer_1")
    retrieved_customer = get_customer(conn, "customer_1")
    assert retrieved_customer == customer
    conn.close()


def test_account_requires_existing_customer(tmp_path):
    db_path = tmp_path / "test_bank_db"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    account = Account("account_1", "nonexistentcustomer_1")
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY constraint failed"):
        insert_account(conn, account)
    conn.close()


def test_account_survives_reopen(tmp_path):
    db_path = tmp_path / "test_bank_db_2"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    customer = Customer("customer_1", "alice")
    account = Account("account_1", "customer_1")
    insert_customer(conn, customer)
    insert_account(conn, account)
    conn.commit()
    conn.close()
    db_path = tmp_path / "test_bank_db_2"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    retrieved_account = get_account(conn, "account_1")
    assert retrieved_account == account
    conn.close()
