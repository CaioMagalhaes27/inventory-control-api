from datetime import date, timedelta

from behave import given, when, then


def _build_payload(product_id: str, quantity: int, minimum_stock: int, expiration_date=None):
    payload = {
        "productId": product_id,
        "quantity": quantity,
        "minimumStock": minimum_stock,
    }
    if expiration_date is not None:
        payload["expirationDate"] = expiration_date
    return payload


@given("the stock is empty")
def step_empty_stock(context):
    response = context.client.get("/api/stock-items")
    assert response.status_code == 200
    assert response.json() == []


@given(
    'a stock item exists for product "{product_id}" with quantity {quantity:d} '
    "and minimum stock {minimum_stock:d}"
)
def step_item_exists(context, product_id, quantity, minimum_stock):
    payload = _build_payload(product_id, quantity, minimum_stock)
    response = context.client.post("/api/stock-items", json=payload)
    assert response.status_code == 201, response.text
    context.last_item = response.json()


@given('a stock item exists for product "{product_id}" expiring in {days:d} days')
def step_item_expiring(context, product_id, days):
    expiration = (date.today() + timedelta(days=days)).isoformat()
    payload = _build_payload(product_id, 10, 5, expiration)
    response = context.client.post("/api/stock-items", json=payload)
    assert response.status_code == 201, response.text
    context.last_item = response.json()


@when(
    'I create a stock item for product "{product_id}" with quantity {quantity:d} '
    "and minimum stock {minimum_stock:d}"
)
def step_create_item(context, product_id, quantity, minimum_stock):
    payload = _build_payload(product_id, quantity, minimum_stock)
    context.response = context.client.post("/api/stock-items", json=payload)


@when("I register an entry of {quantity:d} for the existing stock item")
def step_register_entry(context, quantity):
    item_id = context.last_item["id"]
    context.response = context.client.post(
        f"/api/stock-items/{item_id}/entries",
        json={"quantity": quantity, "reason": "bdd"},
    )


@when("I register an exit of {quantity:d} for the existing stock item")
def step_register_exit(context, quantity):
    item_id = context.last_item["id"]
    context.response = context.client.post(
        f"/api/stock-items/{item_id}/exits",
        json={"quantity": quantity, "reason": "bdd"},
    )


@when("I list low stock items")
def step_list_low_stock(context):
    context.response = context.client.get("/api/stock-items/low-stock")


@when("I list expiring items")
def step_list_expiring(context):
    context.response = context.client.get("/api/stock-items/expiring")


@then("the response status should be {status:d}")
def step_response_status(context, status):
    assert context.response.status_code == status, (
        f"expected {status}, got {context.response.status_code}: {context.response.text}"
    )


@then('the response body should have field "{field}" equal to "{value}"')
def step_body_field(context, field, value):
    body = context.response.json()
    assert str(body.get(field)) == value, body


@then('the error code should be "{code}"')
def step_error_code(context, code):
    body = context.response.json()
    assert body.get("code") == code, body


@then("the stock quantity should be {quantity:d}")
def step_stock_quantity(context, quantity):
    item_id = context.last_item["id"]
    response = context.client.get(f"/api/stock-items/{item_id}")
    assert response.status_code == 200, response.text
    assert response.json()["quantity"] == quantity, response.json()


@then("the number of items returned should be {count:d}")
def step_items_count(context, count):
    body = context.response.json()
    assert isinstance(body, list)
    assert len(body) == count, body
