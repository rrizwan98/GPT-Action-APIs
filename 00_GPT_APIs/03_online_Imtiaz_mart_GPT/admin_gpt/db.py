# db.py
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Optional

# Database URL
DATABASE_URL = "postgresql://neondb_owner:kz7jBqK5RQNM@ep-flat-snow-a59h4e3g.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class GroceryData(SQLModel, table=True):
    __tablename__ = "grocery_data"
    product_id: Optional[int] = Field(default=None, primary_key=True)
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str
