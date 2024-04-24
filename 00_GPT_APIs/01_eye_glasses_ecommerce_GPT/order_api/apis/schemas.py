from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from apis.models import Glasses, GlassType  # Import models and enums
from apis.database import SessionLocal  # Import your database session
from pydantic import BaseModel, conlist
from typing import List
import datetime

class GlassesModel(BaseModel):
    type: GlassType
    material: str
    frame_shape: str
    lens_color: str
    brand: str
    price: float
    colors_available: List[str]
    stock: int
    frame_width: int
    bridge_width: int
    temple_length: int
    lens_height: int
    lens_width: int
    review_rating: float

class OrderCreate(BaseModel):
    user_id: int
    address: str
    payment_method: str
    total_price: float  # Assuming you calculate this on the client side for simplicity

class Item(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    user_id: int
    address: str
    payment_method: str
    items: List[Item]
class ProductDetail(BaseModel):
    product_id: int
    frame_shape: str
    material: str
    lens_color: str
    price: float
    stock: int

class OrderItemDisplay(BaseModel):
    product: ProductDetail  # Ensure this matches the structure being passed
    quantity: int

class OrderDisplay(BaseModel):
    order_id: int
    tracking_number: str
    status: str
    delivery_days: str
    total_price: float
    created_at: str
    items: List[OrderItemDisplay]

    class Config:
        orm_mode = True

