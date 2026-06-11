def test_create_valid_product(client, valid_payload):
    response = client.post("/api/products", json=valid_payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"]
    assert body["name"] == valid_payload["name"]
    assert body["sku"] == valid_payload["sku"]
    assert body["minimumStock"] == valid_payload["minimumStock"]
    assert body["active"] is True


def test_name_required(client, valid_payload):
    valid_payload["name"] = ""
    response = client.post("/api/products", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_sku_required(client, valid_payload):
    valid_payload["sku"] = ""
    response = client.post("/api/products", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_duplicate_sku(client, valid_payload):
    first = client.post("/api/products", json=valid_payload)
    assert first.status_code == 201
    second = client.post("/api/products", json=valid_payload)
    assert second.status_code == 409
    assert second.json()["code"] == "DUPLICATE_SKU"


def test_negative_minimum_stock(client, valid_payload):
    valid_payload["minimumStock"] = -1
    response = client.post("/api/products", json=valid_payload)
    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_list_products(client, valid_payload):
    client.post("/api/products", json=valid_payload)
    second = dict(valid_payload, sku="SKU-002", name="Feijao")
    client.post("/api/products", json=second)
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_product_by_id(client, valid_payload):
    created = client.post("/api/products", json=valid_payload).json()
    response = client.get(f"/api/products/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_product_not_found(client):
    response = client.get("/api/products/missing-id")
    assert response.status_code == 404
    assert response.json()["code"] == "PRODUCT_NOT_FOUND"


def test_update_product(client, valid_payload):
    created = client.post("/api/products", json=valid_payload).json()
    response = client.put(
        f"/api/products/{created['id']}", json={"name": "Arroz Premium"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Arroz Premium"


def test_update_product_not_found(client):
    response = client.put("/api/products/missing", json={"name": "X"})
    assert response.status_code == 404
    assert response.json()["code"] == "PRODUCT_NOT_FOUND"


def test_soft_delete_product(client, valid_payload):
    created = client.post("/api/products", json=valid_payload).json()
    response = client.delete(f"/api/products/{created['id']}")
    assert response.status_code == 204
    listed = client.get("/api/products").json()
    assert listed == []
    again = client.delete(f"/api/products/{created['id']}")
    assert again.status_code == 404


def test_delete_product_not_found(client):
    response = client.delete("/api/products/missing")
    assert response.status_code == 404
    assert response.json()["code"] == "PRODUCT_NOT_FOUND"
