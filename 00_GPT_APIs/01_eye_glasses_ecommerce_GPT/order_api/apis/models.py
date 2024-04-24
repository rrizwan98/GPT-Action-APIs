from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Numeric, ARRAY, Enum, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
import datetime
import enum

Base = declarative_base()

class GlassType(enum.Enum):
    men = "men"
    women = "women"
    eyeglasses = "eyeglasses"
    sunglasses = "sunglasses"

class Glasses(Base):
    __tablename__ = "glasses"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(GlassType))  
    material = Column(String)
    frame_shape = Column(String)
    lens_color = Column(String)
    brand = Column(String)
    price = Column(Numeric)
    colors_available = Column(ARRAY(String))
    stock = Column(Integer)
    frame_width = Column(Integer)
    bridge_width = Column(Integer)
    temple_length = Column(Integer)
    lens_height = Column(Integer)
    lens_width = Column(Integer)
    review_rating = Column(Numeric)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    orders = relationship("Order", back_populates="user")

class OrderItem(Base):  # Define OrderItem before Order
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('glasses.id'))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    address = Column(String)
    payment_method = Column(String)
    total_price = Column(Float)
    status = Column(String, default='Pending')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    shipping = relationship("Shipping", back_populates="order", uselist=False)  # Ensuring a one-to-one relationship

class Shipping(Base):
    __tablename__ = 'shippings'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)
    tracking_number = Column(String)
    status = Column(String)
    delivery_days = Column(String)
    order = relationship("Order", back_populates="shipping")

DATABASE_URL = "postgresql://neondb_owner:qp9MUge1rCGY@ep-sweet-forest-a5plbn8s.us-east-2.aws.neon.tech/neondb?sslmode=require"

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(engine)