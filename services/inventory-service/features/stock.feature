Feature: Stock items and movements

  Background:
    Given the stock is empty

  Scenario: Create a stock item
    When I create a stock item for product "prod-1" with quantity 10 and minimum stock 5
    Then the response status should be 201
    And the response body should have field "productId" equal to "prod-1"

  Scenario: Register an entry movement
    Given a stock item exists for product "prod-1" with quantity 10 and minimum stock 5
    When I register an entry of 5 for the existing stock item
    Then the response status should be 201
    And the stock quantity should be 15

  Scenario: Register an exit movement
    Given a stock item exists for product "prod-1" with quantity 10 and minimum stock 5
    When I register an exit of 4 for the existing stock item
    Then the response status should be 201
    And the stock quantity should be 6

  Scenario: Prevent exit with insufficient stock
    Given a stock item exists for product "prod-1" with quantity 10 and minimum stock 5
    When I register an exit of 999 for the existing stock item
    Then the response status should be 409
    And the error code should be "INSUFFICIENT_STOCK"

  Scenario: Detect low stock
    Given a stock item exists for product "prod-low" with quantity 2 and minimum stock 5
    When I list low stock items
    Then the response status should be 200
    And the number of items returned should be 1

  Scenario: Detect items close to expiration
    Given a stock item exists for product "prod-near" expiring in 10 days
    And a stock item exists for product "prod-far" expiring in 120 days
    When I list expiring items
    Then the response status should be 200
    And the number of items returned should be 1
