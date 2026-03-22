# Feature Spec: Decision Evaluation

## Goal
Evaluate a submitted transaction and return a deterministic decision (`approved`, `review`, or `rejected`) along with clear reasons.

## Scope
- In:
  - Applying rule-based decision logic
  - Returning decision outcomes and reasons
- Out:
  - Machine learning or AI-based decision logic
  - Dynamically configurable rules

## Decision Logic

### Rejection Rules (highest priority)
A transaction is rejected if any of the following are true:
- account_status is not "active"
- amount is greater than available_balance
Note: Invalid inputs (e.g., amount <= 0) are handled at the API validation layer and return a 422 error. The decision engine only evaluates valid transactions.

### Review Rules
If the transaction is not rejected, it is marked for review if any of the following are true:
- amount >= 5000
- country is not "US"
- new_payee is true AND amount >= 1000
- transaction_type is "wire" AND amount >= 2000

### Approval Rule
A transaction is approved only if none of the rejection or review rules apply.

## Output
- The system returns:
  - decision: one of `approved`, `review`, `rejected`
  - reasons: a list of human-readable explanations for triggered rules

## Acceptance Criteria
- [X] Inactive accounts are rejected
- [X] Transactions exceeding available balance are rejected

- [X] Large transactions are marked for review
- [X] International transactions are marked for review
- [X] New payee transactions meeting threshold are marked for review
- [X] Wire transactions meeting threshold are marked for review
- [X] Transactions with no triggered rules are approved
- [X] Response includes decision reasons when rules are triggered