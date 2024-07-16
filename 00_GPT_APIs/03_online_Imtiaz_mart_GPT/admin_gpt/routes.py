# routes.py
from fastapi import APIRouter, HTTPException, Depends
from db import Session, engine, GroceryData
from sqlmodel import Session, select
from models import GroceryDataCreate, productId
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_session():
    with Session(engine) as session:
        yield session

router = APIRouter()

@router.get("/products/")
def read_products(session: Session = Depends(get_session)):
    products = session.exec(select(GroceryData)).all()
    return products

@router.get("/products/{identifier}")
def read_product(identifier: str, session: Session = Depends(get_session)):
    if identifier.isdigit():
        product = session.get(GroceryData, int(identifier))
    else:
        product = session.exec(select(GroceryData).where(GroceryData.product_name == identifier)).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products/")
def create_product(product: GroceryDataCreate, session: Session = Depends(get_session)):
    db_product = GroceryData.from_orm(product)
    try:
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        logger.info(f"Product added: {db_product}")
        return (f"Product added successfully: {db_product.product_id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error adding product: {e}")
        raise HTTPException(status_code=500, detail="Failed to add product")

@router.put("/products/{productID}")
def update_product(productID: str, product: GroceryDataCreate, session: Session = Depends(get_session)):
    if productID.isdigit():
        db_product = session.get(GroceryData, int(productID))
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_data = product.dict(exclude_unset=True)
    logger.info(f"Updating product ID {productID} with data: {product_data}")
    
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    try:
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
        logger.info(f"Product updated: {db_product}")
        return db_product
    except Exception as e:
        session.rollback()
        logger.error(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail="Failed to update product")

@router.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(GroceryData, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return (f"Product deleted successfully")


