import sqlite3
from pathlib import Path
from storage.database import connect_db, initialize_schema
from domains.models import Customer
from storage.sqlite_repository import insert_customer, get_customer


def test_customer_survives_reopen(tmp_path):
    db_path= tmp_path / "test_bank_db"
    conn = connect_db(str(db_path))
    initialize_schema(conn)
    customer= Customer("customer_1", "alice")
    alice_db= insert_customer(conn, customer)
    conn.commit()
    conn.close()
    db_path_1= tmp_path / "test_bank_db_1"
    conn = connect_db(str(db_path_1))
    initialize_schema(conn)
    get_customer(conn,"customer_1" )

