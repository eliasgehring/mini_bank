from decimal import Decimal
from domains import validate_amount


def money_to_cents(amount: Decimal) -> int:
    validate_amount(amount)
    cents = amount * Decimal("100.00")
    return int(cents)
