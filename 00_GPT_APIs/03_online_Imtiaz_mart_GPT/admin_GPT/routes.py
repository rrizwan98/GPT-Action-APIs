from fastapi import FastAPI, HTTPException
from fastapi import HTTPException, Request
from typing import Union
from admin_GPT.db import get_all_products, get_product_by_name_or_id, add_product
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    category: str
    sub_category: str
    product_name: str
    price: float
    image_url: str

@app.get("/products")
def read_products():
    """ Endpoint to fetch all products """
    try:
        return get_all_products().to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/product")
def read_product(name: Union[str, None] = None, product_id: Union[int, None] = None):
    """ Endpoint to fetch a product by name or ID """
    if not name and not product_id:
        raise HTTPException(status_code=400, detail="Please provide a product name or ID.")
    try:
        result = get_product_by_name_or_id(name, product_id)
        if result.empty:
            raise HTTPException(status_code=404, detail="Product not found.")
        return result.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_product")
def create_product(product_details: Product):
    """ Endpoint to add a new product """
    try:
        response = add_product(product_details.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))