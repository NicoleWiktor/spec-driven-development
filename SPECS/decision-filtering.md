# Feature Spec: Decision Filtering

## Goal
Allow users to filter transactions by decision outcome.

## Scope
- In:
  - Filtering by decision type
- Out:
  - Complex multi-field search

## Behavior
- The system supports filtering transactions by decision:
  - approved
  - review
  - rejected
- Invalid filter values return an error

## Acceptance Criteria
- [X] Filtering by approved returns only approved transactions
- [X] Filtering by review returns only review transactions
- [X] Filtering by rejected returns only rejected transactions
- [X] Invalid filter values return an error