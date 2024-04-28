from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.models import Glasses, GlassType  # Import models and enums
from api.database import SessionLocal  # Import your database session
from pydantic import BaseModel, conlist
from typing import List

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

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/glasses/")
async def create_glasses(glasses: GlassesModel, db: Session = Depends(get_db)):
    db_glasses = Glasses(**glasses.dict())
    db.add(db_glasses)
    db.commit()
    db.refresh(db_glasses)
    return db_glasses
