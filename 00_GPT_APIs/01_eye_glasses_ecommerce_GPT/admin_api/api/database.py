from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Make sure to import Base from models

DATABASE_URL = "postgresql://neondb_owner:qp9MUge1rCGY@ep-sweet-forest-a5plbn8s.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)  # Create tables
