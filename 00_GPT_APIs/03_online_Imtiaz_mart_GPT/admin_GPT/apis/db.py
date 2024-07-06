from sqlalchemy import create_engine
from pandas import read_sql_query
from sqlalchemy import text

# Initialize the database connection
engine = create_engine("postgresql://neondb_owner:kz7jBqK5RQNM@ep-flat-snow-a59h4e3g.us-east-2.aws.neon.tech/neondb?sslmode=require")

def get_all_products():
    """ Fetch all products from the database """
    query = "SELECT * FROM grocery_data"
    return read_sql_query(query, con=engine)

def get_product_by_name_or_id(name=None, product_id=None):
    """ Fetch a single product by name or ID """
    if name:
        query = f"SELECT * FROM grocery_data WHERE product_name = '{name}'"
    elif product_id:
        query = f"SELECT * FROM grocery_data WHERE id = {product_id}"
    else:
        return None
    return read_sql_query(query, con=engine)

def add_product(product_details):
    """ Add a new product to the database """
    query = text("""
        INSERT INTO grocery_data (category, sub_category, product_name, price, image_url)
        VALUES (:category, :sub_category, :product_name, :price, :image_url)
    """)
    with engine.connect() as connection:
        connection.execute(query, product_details)
        connection.commit()  # Explicitly commit the transaction
        return {"message": "Product added successfully!"}
    
def update_product(product_name, product_details):
    """ Update an existing product in the database based on the product name """
    values = {key: value for key, value in product_details.items() if value is not None}
    set_clause = ", ".join([f"{key} = :{key}" for key in values.keys()])
    query = text(f"UPDATE grocery_data SET {set_clause} WHERE TRIM(LOWER(product_name)) = TRIM(LOWER(:product_name))")

    with engine.connect() as connection:
        values['product_name'] = product_name
        print("Executing SQL:", query)
        print("With values:", values)
        result = connection.execute(query, values)
        connection.commit()

        print("Rows affected:", result.rowcount)
        
        if result.rowcount:
            return {"message": "Product updated successfully!"}
        else:
            return {"message": "Product not found or no updates performed."}

def delete_product(product_name):
    """ Delete a product from the database based on the product name """
    query = text("DELETE FROM grocery_data WHERE TRIM(LOWER(product_name)) = TRIM(LOWER(:product_name))")

    with engine.connect() as connection:
        result = connection.execute(query, {'product_name': product_name})
        connection.commit()

        if result.rowcount:
            return {"message": "Product deleted successfully!"}
        else:
            return {"message": "Product not found."}