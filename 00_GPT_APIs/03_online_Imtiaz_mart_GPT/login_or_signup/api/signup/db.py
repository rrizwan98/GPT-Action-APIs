from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

# Connection to Neon PostgreSQL
DATABASE_URL = "postgresql://neondb_owner:kz7jBqK5RQNM@ep-flat-snow-a59h4e3g.us-east-2.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
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

# admin table
admin = Table(
    'admin', metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('email', String, unique=True, index=True),
    Column('username', String, unique=True, index=True),
    Column('password', String),
)

metadata.create_all(bind=engine)

# Function to add user to the database
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

# Function to add user to the database
def create_admin_user(email, username, password):
    db_session = SessionLocal()
    try:
        db_session.execute(admin.insert().values(email=email, username=username, password=password))
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        db_session.rollback()
        return False
    finally:
        db_session.close()

def authenticate_user(email, password):
    db_session = SessionLocal()
    try:
        query = select(users).where(users.c.email == email, users.c.password == password)
        result = db_session.execute(query).fetchone()
        if result:
            # Convert RowProxy to a dictionary using the _mapping attribute
            return dict(result._mapping)
        return None
    finally:
        db_session.close()

def authenticate_admin(email, password):
    db_session = SessionLocal()
    try:
        query = select(admin).where(admin.c.email == email, admin.c.password == password)
        result = db_session.execute(query).fetchone()
        if result:
            # Convert RowProxy to a dictionary using the _mapping attribute
            return dict(result._mapping)
        return None
    finally:
        db_session.close()