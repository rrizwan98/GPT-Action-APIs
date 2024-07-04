import pandas as pd
from sqlalchemy import create_engine, text
# pip install openpyxl
# Load the Excel file
excel_file_path = 'admin_GPT/Product_Details_Extract.xlsx'
data = pd.read_excel(excel_file_path)

# Rename columns to match the database schema
data.columns = ['category', 'sub_category', 'product_name', 'price', 'image_url']

# Define the database connection URL
db_url = "postgresql://neondb_owner:kz7jBqK5RQNM@ep-flat-snow-a59h4e3g.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Create a SQL Alchemy engine
engine = create_engine(db_url)

# SQL to create a table matching the Excel structure
create_table_sql = text("""
CREATE TABLE IF NOT EXISTS grocery_data (
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    price NUMERIC,
    image_url TEXT
);
""")

# Execute the table creation
with engine.connect() as connection:
    connection.execute(create_table_sql)

# Insert data from the DataFrame into the PostgreSQL table
data.to_sql('grocery_data', con=engine, if_exists='append', index=False)

# Optionally, check if data was inserted successfully by retrieving the first few rows
with engine.connect() as connection:
    result = pd.read_sql("SELECT * FROM grocery_data LIMIT 5", con=connection)
    print("successfully save all the data in db", result)
