from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from login_or_signup.api.signup.db import create_user, create_admin_user, authenticate_user, authenticate_admin

app = FastAPI()

class User(BaseModel):
    email: str
    username: str
    password: str

@app.post("/signup/users")
async def signup(user: User):
    success = create_user(user.email, user.username, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Error creating user")
    return {"message": "User created successfully"}

@app.post("/signup/admin")
async def signup(user: User):
    success = create_admin_user(user.email, user.username, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Error creating user")
    return {"message": "admin User created successfully"}


class Login(BaseModel):
    email: str
    password: str

@app.post("/user/login/")
async def user_login(credentials: Login):
    user = authenticate_user(credentials.email, credentials.password)
    if user:
        return {"message": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
@app.post("/admin/login/")
async def admin_login(credentials: Login):
    admin = authenticate_admin(credentials.email, credentials.password)
    if admin:
        # Convert SQLAlchemy Row Proxy to dict if not done in the function
        admin_data = dict(admin) if not isinstance(admin, dict) else admin
        return {"message": "Admin Login successful", "user": admin_data}
    else:
        raise HTTPException(status_code=404, detail="Invalid credentials")
