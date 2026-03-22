# Feature Spec: Transaction Retrieval

## Goal
Allow users to retrieve stored transactions and their decisions.

## Scope
- In:
  - Retrieving all transactions
  - Retrieving a transaction by ID
- Out:
  - Pagination
  - Sorting

## Behavior

### Retrieve All Transactions
- Returns all stored transactions
- Includes decision and reasons for each

### Retrieve by ID
- Returns a single transaction by ID
- If the ID does not exist, return a not-found error

## Acceptance Criteria
- [X] User can retrieve all transactions
- [X] User can retrieve a transaction by ID
- [X] Returned transactions include decision and reasons
- [X] Non-existent IDs return a not-found error

