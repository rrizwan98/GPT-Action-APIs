Feature: Product management
  As an API client
  I want to manage products

  Scenario: Get all products
    Given I have product data
    When I request all products
    Then I should receive a list of products

  Scenario: Get a single product by ID
    Given I have product data
    When I request a product with ID "2"
    Then I should receive the product details

  Scenario: Create a product
    Given I have new product details
    When I create a product
    Then I should receive a successful creation message

  Scenario: Update a product by ID
    Given I have existing product data
    When I update a product with ID "1002"
    Then I should receive updated product details

  Scenario: Delete a product by ID
    Given I have product data
    When I delete a product with ID "1002"
    Then I should receive a successful deletion message

