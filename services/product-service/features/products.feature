Feature: Product catalog management

  Background:
    Given the product catalog is empty

  Scenario: Create a valid product
    When I create a product with name "Arroz 1kg" sku "SKU-001" unit "kg" and minimum stock 5
    Then the response status should be 201
    And the response body should have field "sku" equal to "SKU-001"

  Scenario: Reject duplicate SKU
    Given a product exists with sku "SKU-001"
    When I create a product with name "Arroz 1kg" sku "SKU-001" unit "kg" and minimum stock 5
    Then the response status should be 409
    And the error code should be "DUPLICATE_SKU"

  Scenario: List products
    Given a product exists with sku "SKU-001"
    And a product exists with sku "SKU-002"
    When I list products
    Then the response status should be 200
    And the number of products returned should be 2

  Scenario: Fetch a product that does not exist
    When I fetch the product with id "missing-id"
    Then the response status should be 404
    And the error code should be "PRODUCT_NOT_FOUND"

  Scenario: Update an existing product
    Given a product exists with sku "SKU-001"
    When I update the existing product name to "Arroz Premium"
    Then the response status should be 200
    And the response body should have field "name" equal to "Arroz Premium"

  Scenario: Soft delete a product
    Given a product exists with sku "SKU-001"
    When I delete the existing product
    Then the response status should be 204
    And listing products should return 0 items
