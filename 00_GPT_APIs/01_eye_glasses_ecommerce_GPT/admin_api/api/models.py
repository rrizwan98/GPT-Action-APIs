from sqlalchemy import Column, Integer, String, Numeric, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base
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
