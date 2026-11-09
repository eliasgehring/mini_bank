import sqlite3
from typing import Optional 

from domains.models import Customer 

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


def get_customer(
conn: sqlite3.Connection,
customer_id: str,       
) -> Optional[Customer]:

    row= conn.execute(
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