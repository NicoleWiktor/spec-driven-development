# Transaction Review Service

This is a backend service that accepts transaction requests and decides whether to approve, review, or reject them based on predefined business rules.


It was built using a spec-driven workflow, where each feature was defined before implementation and validated with tests.

## What It Does
- Accepts transaction data through an API
- Applies deterministic rules to evaluate the risk of the transaction
- Stores transactions in a SQLite database
- Allows retrieval and filtering of transactions
- Provides a summary of decisions

## Tech Stack
- FastAPI
- SQLAlchemy + SQLite
- Pydantic
- Pytest + TestClient

## Run Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use /docs to explore endpoints.

API: `http://127.0.0.1:8000`  
Docs: `http://127.0.0.1:8000/docs`

SQLite database file is created at `transactions.db`.

## Run Tests
```bash
pytest -q
```

## Main Endpoints
- `POST /transactions` - create and evaluate a transaction
- `GET /transactions` - list transactions (optional `?decision=approved|review|rejected`)
- `GET /transactions/{transaction_id}` - fetch one transaction by ID
- `GET /transactions/summary` - return aggregate counts by decision

## Request Fields (`POST /transactions`)
- `account_id` (string)
- `amount` (number, must be `> 0`)
- `country` (string)
- `available_balance` (number)
- `account_status` (string)
- `transaction_type` (string)
- `new_payee` (boolean)


## How To Submit A Transaction
Send a `POST` request to `/transactions` with JSON body.

Valid example:
```json
{
  "account_id": "acct-100",
  "amount": 250.0,
  "country": "US",
  "available_balance": 1000.0,
  "account_status": "active",
  "transaction_type": "card",
  "new_payee": false
}
```

Invalid example (`amount <= 0`):
```json
{
  "account_id": "acct-100",
  "amount": 0,
  "country": "US",
  "available_balance": 1000.0,
  "account_status": "active",
  "transaction_type": "card",
  "new_payee": false
}
```

Expected error response:
```json
{
  "detail": "amount must be greater than 0"
}
```

## Decision Rules

### Rejected
- `account_status != "active"`
- `amount > available_balance`

### Review (only if not rejected)
- `amount >= 5000`
- `country != "US"`
- `new_payee == true` and `amount >= 1000`
- `transaction_type == "wire"` and `amount >= 2000`

### Approved
- no rules triggered

## Response Shape
- `POST /transactions` and retrieval endpoints return:
  - `id` (int)
  - `decision` (`approved` | `review` | `rejected`)
  - `reasons` (list of strings)

## Error Behavior
- Invalid body/field types: `422`
- `amount <= 0`: `422` with `"amount must be greater than 0"`
- Invalid decision filter: `422`
- Unknown transaction ID: `404` with `"Transaction not found."`
