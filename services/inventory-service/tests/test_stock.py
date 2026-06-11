from datetime import date, timedelta


def test_create_valid_stock_item(client, valid_payload):
    response = client.post("/api/stock-items", json=valid_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["productId"] == "prod-1"
    assert body["quantity"] == 10


def test_product_id_required(client, valid_payload):
    valid_payload["productId"] = ""
    response = client.post("/api/stock-items", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_negative_quantity(client, valid_payload):
    valid_payload["quantity"] = -1
    response = client.post("/api/stock-items", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_negative_minimum_stock(client, valid_payload):
    valid_payload["minimumStock"] = -1
    response = client.post("/api/stock-items", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_list_stock_items(client, valid_payload):
    client.post("/api/stock-items", json=valid_payload)
    second = dict(valid_payload, productId="prod-2", batchCode="B-002")
    client.post("/api/stock-items", json=second)
    response = client.get("/api/stock-items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_by_id(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.get(f"/api/stock-items/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_not_found(client):
    response = client.get("/api/stock-items/missing")
    assert response.status_code == 404
    assert response.json()["code"] == "STOCK_ITEM_NOT_FOUND"


def test_valid_entry(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.post(
        f"/api/stock-items/{created['id']}/entries",
        json={"quantity": 5, "reason": "purchase"},
    )
    assert response.status_code == 201
    movement = response.json()
    assert movement["type"] == "ENTRY"
    assert movement["quantity"] == 5

    refreshed = client.get(f"/api/stock-items/{created['id']}").json()
    assert refreshed["quantity"] == 15


def test_invalid_entry(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.post(
        f"/api/stock-items/{created['id']}/entries", json={"quantity": 0}
    )
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_valid_exit(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.post(
        f"/api/stock-items/{created['id']}/exits",
        json={"quantity": 4, "reason": "sale"},
    )
    assert response.status_code == 201
    assert response.json()["type"] == "EXIT"

    refreshed = client.get(f"/api/stock-items/{created['id']}").json()
    assert refreshed["quantity"] == 6


def test_invalid_exit(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.post(
        f"/api/stock-items/{created['id']}/exits", json={"quantity": 0}
    )
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_insufficient_stock(client, valid_payload):
    created = client.post("/api/stock-items", json=valid_payload).json()
    response = client.post(
        f"/api/stock-items/{created['id']}/exits", json={"quantity": 999}
    )
    assert response.status_code == 409
    assert response.json()["code"] == "INSUFFICIENT_STOCK"


def test_low_stock_endpoint(client, valid_payload):
    payload = dict(valid_payload, quantity=2, minimumStock=5)
    client.post("/api/stock-items", json=payload)
    response = client.get("/api/stock-items/low-stock")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_expiring_endpoint(client, valid_payload, near_expiration_date):
    payload = dict(valid_payload, expirationDate=near_expiration_date)
    client.post("/api/stock-items", json=payload)
    far_payload = dict(
        valid_payload,
        productId="prod-far",
        batchCode="B-FAR",
        expirationDate=(date.today() + timedelta(days=120)).isoformat(),
    )
    client.post("/api/stock-items", json=far_payload)
    response = client.get("/api/stock-items/expiring")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["expirationDate"] == near_expiration_date


def test_past_expiration_rejected(client, valid_payload):
    past = (date.today() - timedelta(days=1)).isoformat()
    payload = dict(valid_payload, expirationDate=past)
    response = client.post("/api/stock-items", json=payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"
