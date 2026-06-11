from behave import given, when, then


@given("the product catalog is empty")
def step_empty_catalog(context):
    response = context.client.get("/api/products")
    assert response.status_code == 200
    assert response.json() == []


@given('a product exists with sku "{sku}"')
def step_product_exists(context, sku):
    payload = {
        "name": f"Product {sku}",
        "sku": sku,
        "unit": "kg",
        "minimumStock": 5,
    }
    response = context.client.post("/api/products", json=payload)
    assert response.status_code == 201, response.text
    context.created[sku] = response.json()
    context.last_created = response.json()


@when(
    'I create a product with name "{name}" sku "{sku}" unit "{unit}" '
    "and minimum stock {minimum_stock:d}"
)
def step_create_product(context, name, sku, unit, minimum_stock):
    payload = {
        "name": name,
        "sku": sku,
        "unit": unit,
        "minimumStock": minimum_stock,
    }
    context.response = context.client.post("/api/products", json=payload)


@when("I list products")
def step_list_products(context):
    context.response = context.client.get("/api/products")


@when('I fetch the product with id "{product_id}"')
def step_fetch_product(context, product_id):
    context.response = context.client.get(f"/api/products/{product_id}")


@when('I update the existing product name to "{name}"')
def step_update_product(context, name):
    product_id = context.last_created["id"]
    context.response = context.client.put(
        f"/api/products/{product_id}", json={"name": name}
    )


@when("I delete the existing product")
def step_delete_product(context):
    product_id = context.last_created["id"]
    context.response = context.client.delete(f"/api/products/{product_id}")


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


@then("the number of products returned should be {count:d}")
def step_count_products(context, count):
    body = context.response.json()
    assert isinstance(body, list)
    assert len(body) == count, body


@then("listing products should return {count:d} items")
def step_listing_count(context, count):
    response = context.client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) == count
