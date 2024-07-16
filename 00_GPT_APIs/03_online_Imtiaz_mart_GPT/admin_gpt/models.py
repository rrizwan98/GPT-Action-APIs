# models.py
from pydantic import BaseModel, HttpUrl

class productId(BaseModel):
    productId: int

class GroceryDataCreate(BaseModel):
    product_id: int
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str

    class Config:
        orm_mode = True
