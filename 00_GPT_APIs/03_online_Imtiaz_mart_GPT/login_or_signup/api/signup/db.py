from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
# import api.signup.setting


DATABASE_URL = "postgresql://imtiaz:imtiaz@localhost:5432/onlineMart?sslmode=disable"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database schema
metadata = MetaData()
users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', String, unique=True, index=True),
    Column('username', String, unique=True, index=True),
    Column('password', String),
)

metadata.create_all(bind=engine)

# Function to add user to database
def create_user(email, username, password):
    db_session = SessionLocal()
    try:
        db_session.execute(users.insert().values(email=email, username=username, password=password))
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        db_session.rollback()
        return False
    finally:
        db_session.close()
