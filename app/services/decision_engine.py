from ..schemas import TransactionCreate


def evaluate_transaction(payload: TransactionCreate) -> tuple[str, list[str]]:
    reject_reasons: list[str] = []

    if payload.account_status.strip().lower() != "active":
        reject_reasons.append("Rejected: account status is not active.")
    if payload.amount <= 0:
        reject_reasons.append("Rejected: amount must be greater than 0.")
    if payload.amount > payload.available_balance:
        reject_reasons.append("Rejected: amount exceeds available balance.")

    if reject_reasons:
        return "rejected", reject_reasons

    review_reasons: list[str] = []

    if payload.amount >= 5000:
        review_reasons.append("Review: amount is 5000 or higher.")
    if payload.country.strip().upper() != "US":
        review_reasons.append("Review: transaction country is not US.")
    if payload.new_payee and payload.amount >= 1000:
        review_reasons.append("Review: new payee transaction is 1000 or higher.")
    if payload.transaction_type.strip().lower() == "wire" and payload.amount >= 2000:
        review_reasons.append("Review: wire transaction is 2000 or higher.")

    if review_reasons:
        return "review", review_reasons

    return "approved", []
