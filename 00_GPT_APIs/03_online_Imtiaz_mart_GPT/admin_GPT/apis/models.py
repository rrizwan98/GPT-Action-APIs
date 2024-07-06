from pydantic import BaseModel, Field
from typing import Optional

class ProductUpdate(BaseModel):
    category: Optional[str] = Field(None, description="Category of the product")
    sub_category: Optional[str] = Field(None, description="Sub-category of the product")
    product_name: Optional[str] = Field(None, description="Name of the product")
    price: Optional[float] = Field(None, description="Price of the product")
    image_url: Optional[str] = Field(None, description="URL of the product image")

class Product(BaseModel):
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str
