# Feature Spec: Transaction Summary

## Goal
Provide a summary of stored transactions.

## Scope
- In:
  - Aggregating transaction counts by decision
  - Returning total transaction count
- Out:
  - Modifying transactions
  - Advanced analytics or historical trends

## Requirements
- The system must provide a summary endpoint for transactions.
- The summary must include:
  - total transaction count
  - approved transaction count
  - review transaction count
  - rejected transaction count

## Acceptance Criteria
- [X] User can retrieve transaction summary
- [X] Summary includes total, approved, review, and rejected counts
- [X] Summary values accurately reflect stored transaction data