# routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from apis.models import Glasses, Order, OrderItem, User, Shipping
from apis.schemas import GlassesModel, OrderCreate, OrderDisplay, ProductDetail, OrderItemDisplay
from apis.database import SessionLocal
from typing import List, Any
import datetime
import random
import string

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/products/", response_model=List[GlassesModel])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Glasses).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=GlassesModel)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Glasses).filter(Glasses.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/cart/", response_model=Any)
def add_to_cart(product_id: int, quantity: int, db: Session = Depends(get_db)):
    # Check if the product exists in the database
    product = db.query(Glasses).filter(Glasses.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the stock is sufficient
    if product.stock < quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock available! Only {product.stock} left.")

    # Logic to add to cart (assuming a simple dictionary for cart representation)
    # This part would typically interact with a cart model or a persistent storage system
    cart = {"product_id": product_id, "quantity": quantity, "name": product.frame_shape, "price": float(product.price)}
    
    # Here you might want to update the stock in the database, reflect cart addition etc.
    # This example will just return the cart item as a demonstration
    return cart
def generate_tracking_number():
    """Generate a random tracking number."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

@router.post("/orders/", response_model=OrderDisplay)
def create_order(order_details: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == order_details.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_order = Order(
        user_id=user.id,
        address=order_details.address,
        payment_method=order_details.payment_method,
        total_price=0,
        status='Pending',
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_order)
    db.commit()

    order_items = []
    total_price = 0
    for item in order_details.items:
        glasses = db.query(Glasses).filter(Glasses.id == item.product_id).first()
        if not glasses:
            raise HTTPException(status_code=404, detail="Product not found")
        if glasses.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        glasses.stock -= item.quantity
        db.add(glasses)

        # Create ProductDetail instance
        product_detail = ProductDetail(
            product_id=glasses.id,
            frame_shape=glasses.frame_shape,
            material=glasses.material,
            lens_color=glasses.lens_color,
            price=float(glasses.price),
            stock=glasses.stock
        )

        # Append OrderItemDisplay
        order_items.append(OrderItemDisplay(product=product_detail, quantity=item.quantity))

    new_order.total_price = total_price
    db.commit()

    return OrderDisplay(
        order_id=new_order.id,
        tracking_number="XYZ123",
        status="In Transit",
        delivery_days="2 working days",
        total_price=total_price,
        created_at=new_order.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        items=order_items
    )


@router.get("/orders/history/{user_id}", response_model=List[OrderDisplay])
def order_history(user_id: int, db: Session = Depends(get_db)):
    # Use joinedload to fetch related data in a single query to improve performance
    orders = db.query(Order).options(joinedload(Order.items).joinedload(OrderItem.product_id),
                                     joinedload(Order.shipping)).filter(Order.user_id == user_id).all()
    
    if not orders:
        raise HTTPException(status_code=404, detail="No orders found for this user")

    # Return the orders, using the response model to ensure correct data format
    return orders
@router.post("/users/register/")
def register_user(email: str, password: str):
    return {"email": email, "status": "Registered"}

@router.post("/users/login/")
def login_user(email: str, password: str):
    return {"email": email, "status": "Logged in"}
