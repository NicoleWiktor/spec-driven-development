# Feature Spec: Health Check

## Goal
Provide a simple endpoint to verify that the service is running.

## Endpoint
GET /

## Response
{
  "message": "Transaction Review Service is running. See /docs for API usage."
}

## Acceptance Criteria
- [X] GET / returns status 200
- [X] Response includes a message indicating the service is running