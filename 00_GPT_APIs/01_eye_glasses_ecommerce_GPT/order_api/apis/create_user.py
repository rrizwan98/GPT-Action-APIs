from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User, Base

# Assuming your DATABASE_URL and models are correctly set up
DATABASE_URL = "postgresql://neondb_owner:qp9MUge1rCGY@ep-sweet-forest-a5plbn8s.us-east-2.aws.neon.tech/neondb?sslmode=require"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def add_dummy_user():
    db = SessionLocal()
    new_user = User(id=1)  # You can add more attributes here if needed, such as name, email, etc.
    db.add(new_user)
    db.commit()
    db.close()
    print("User added successfully!")

if __name__ == "__main__":
    add_dummy_user()
