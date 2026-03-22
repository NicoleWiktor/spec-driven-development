def build_payload(**overrides):
    payload = {
        "account_id": "acct-123",
        "amount": 100.0,
        "country": "US",
        "available_balance": 1000.0,
        "account_status": "active",
        "transaction_type": "card",
        "new_payee": False,
    }
    payload.update(overrides)
    return payload


def create_transaction(client, **overrides):
    return client.post("/transactions", json=build_payload(**overrides))


def test_valid_transaction_submission_succeeds(client):
    response = create_transaction(client)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["decision"] in {"approved", "review", "rejected"}
    assert isinstance(body["reasons"], list)


def test_missing_required_field_returns_error(client):
    payload = build_payload()
    payload.pop("account_id")
    response = client.post("/transactions", json=payload)
    assert response.status_code == 422


def test_invalid_field_type_returns_error(client):
    response = create_transaction(client, amount="not-a-number")
    assert response.status_code == 422


def test_non_positive_amount_returns_error(client):
    response = create_transaction(client, amount=0)
    assert response.status_code == 422


def test_inactive_account_is_rejected(client):
    response = create_transaction(client, account_status="inactive")
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "rejected"
    assert any("account status is not active" in reason.lower() for reason in body["reasons"])


def test_transaction_exceeding_available_balance_is_rejected(client):
    response = create_transaction(client, amount=1500, available_balance=1000)
    assert response.status_code == 201
    body = response.json()
    assert body["decision"] == "rejected"
    assert any("exceeds available balance" in reason.lower() for reason in body["reasons"])


def test_amount_ge_5000_is_marked_for_review(client):
    response = create_transaction(client, amount=5000, available_balance=10000)
    assert response.status_code == 201
    assert response.json()["decision"] == "review"


def test_non_us_country_is_marked_for_review(client):
    response = create_transaction(client, country="CA")
    assert response.status_code == 201
    assert response.json()["decision"] == "review"


def test_new_payee_with_amount_ge_1000_is_marked_for_review(client):
    response = create_transaction(client, new_payee=True, amount=1000)
    assert response.status_code == 201
    assert response.json()["decision"] == "review"


def test_wire_transaction_with_amount_ge_2000_is_marked_for_review(client):
    response = create_transaction(
        client,
        transaction_type="wire",
        amount=2000,
        available_balance=5000,
    )
    assert response.status_code == 201
    assert response.json()["decision"] == "review"


def test_transaction_with_no_triggered_rules_is_approved(client):
    response = create_transaction(client, amount=250, country="US", transaction_type="card", new_payee=False)
    assert response.status_code == 201
    assert response.json()["decision"] == "approved"


def test_get_all_transactions_returns_stored_transactions(client):
    create_transaction(client)
    create_transaction(client, country="CA")

    response = client.get("/transactions")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2


def test_get_transaction_by_id_returns_correct_record(client):
    first = create_transaction(client).json()
    create_transaction(client, country="CA")

    response = client.get(f"/transactions/{first['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == first["id"]


def test_non_existent_transaction_id_returns_404(client):
    response = client.get("/transactions/999999")
    assert response.status_code == 404


def test_decision_approved_returns_only_approved_transactions(client):
    approved = create_transaction(client, amount=100, country="US").json()
    create_transaction(client, country="CA")
    create_transaction(client, account_status="inactive")

    response = client.get("/transactions?decision=approved")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == approved["id"]
    assert all(item["decision"] == "approved" for item in body)


def test_decision_review_returns_only_review_transactions(client):
    create_transaction(client, amount=100, country="US")
    review = create_transaction(client, country="CA").json()
    create_transaction(client, account_status="inactive")

    response = client.get("/transactions?decision=review")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == review["id"]
    assert all(item["decision"] == "review" for item in body)


def test_decision_rejected_returns_only_rejected_transactions(client):
    create_transaction(client, amount=100, country="US")
    create_transaction(client, country="CA")
    rejected = create_transaction(client, account_status="inactive").json()

    response = client.get("/transactions?decision=rejected")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == rejected["id"]
    assert all(item["decision"] == "rejected" for item in body)


def test_invalid_decision_filter_returns_error(client):
    response = client.get("/transactions?decision=unknown")
    assert response.status_code == 422
