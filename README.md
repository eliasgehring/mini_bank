# Mini Bank

A minimal banking engine written in Python, exploring financial systems and software engineering from first principles.

The original implementation was written independently, without AI-assisted coding.

## Design Principles

- Immutable financial domain models
- Transaction-derived account balances
- Decimal-based monetary arithmetic
- Monetary conservation across transfers
- Explicit financial and chronological invariants
- Validation before state mutation
- Separation of domain logic, services and persistence

## Architecture

| Module | Responsibility |
|---|---|
| `domains/` | Financial entities and invariants |
| `services/` | Banking operations and balance computation |
| `storage/` | SQLite schema and persistence |
| `bank_state.py` | In-memory state |
| `tests/` | Automated verification |

## Getting Started

```bash
python -m pip install -r requirements-dev.txt
python main.py
python -m pytest -q
```

## Testing

35 automated tests covering financial invariants, transaction integrity, monetary conservation, account isolation and database persistence.

## Development Status

The transaction engine currently operates in memory. SQLite persistence for customers and accounts is implemented. Full transactional persistence remains under development.

This project is educational and is not intended for production banking operations.