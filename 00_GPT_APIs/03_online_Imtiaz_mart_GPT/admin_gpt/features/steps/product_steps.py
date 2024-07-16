from behave import *
import requests

api_url = "https://adminapi.blackflower-9e2d4f52.eastus2.azurecontainerapps.io"

@given('I have product data')
def step_impl(context):
    pass  # Assuming data is already in the database or mocked

@when('I request all products')
def step_impl(context):
    context.response = requests.get(f"{api_url}/products/")

@then('I should receive a list of products')
def step_impl(context):
    assert context.response.status_code == 200
    assert isinstance(context.response.json(), list)

@when('I request a product with ID "{product_id}"')
def step_impl(context, product_id):
    context.response = requests.get(f"{api_url}/products/{product_id}")

@then('I should receive the product details')
def step_impl(context):
    assert context.response.status_code == 200
    assert 'product_id' in context.response.json()

@given('I have new product details')
def step_impl(context):
    # Assuming the product details to be used in a POST request
    context.new_product = {
        "product_id": 1001,
        "category": "Food",
        "sub_category": "Snacks",
        "product_name": "Chips",
        "price": 2.5,
        "image_url": "http://example.com/chips.jpg"
    }

@when('I create a product')
def step_impl(context):
    product_data = {
        "product_id": 1002,
        "category": "Food",
        "sub_category": "Snacks",
        "product_name": "potato Chips",
        "price": 50,
        "image_url": "http://example.com/chips.jpg"
    }
    context.response = requests.post(f"{api_url}/products/", json=product_data)

@then('I should receive a successful creation message')
def step_impl(context):
    assert context.response.status_code == 200
    assert 'Product added successfully' in context.response.text

@given('I have existing product data')
def step_impl(context):
    # Here, you might want to set up or ensure the product exists for update
    context.product_id = "1002"  # Example product ID
    context.product_update_data = {
        "product_id": 1002,
        "category": "Beverages",
        "sub_category": "Tea",
        "product_name": "Green Tea",
        "price": 100.50,
        "image_url": "http://example.com/greentea.jpg"
    }

@when('I update a product with ID "{product_id}"')
def step_impl(context, product_id):
    context.response = requests.put(f"{api_url}/products/{product_id}", json=context.product_update_data)

@then('I should receive updated product details')
def step_impl(context):
    assert context.response.status_code == 200
    response_data = context.response.json()
    # Check that some details are indeed the updated ones
    assert response_data["product_name"] == context.product_update_data["product_name"]
    assert response_data["price"] == context.product_update_data["price"]

@when('I delete a product with ID "{product_id}"')
def step_impl(context, product_id):
    context.response = requests.delete(f"{api_url}/products/{product_id}")

@then('I should receive a successful deletion message')
def step_impl(context):
    assert context.response.status_code == 200
    assert "Product deleted successfully" in context.response.text
