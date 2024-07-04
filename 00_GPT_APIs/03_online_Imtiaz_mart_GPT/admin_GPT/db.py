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