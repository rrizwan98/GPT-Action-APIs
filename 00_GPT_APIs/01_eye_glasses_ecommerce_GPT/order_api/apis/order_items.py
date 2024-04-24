# in order_items.py
from models import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class OrderItem(Base):
    __tablename__ = 'order_items'
    order = relationship("Order", back_populates="items")  # Assume Order will be defined later

# in orders.py
from .order_items import OrderItem  # Import OrderItem before defining Order
from models import Base  # Make sure to import Base from models
from models import User  # Make sure to import Base from models
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = 'orders'
    items = relationship("OrderItem", back_populates="order")
    user = relationship("User", back_populates="orders")
