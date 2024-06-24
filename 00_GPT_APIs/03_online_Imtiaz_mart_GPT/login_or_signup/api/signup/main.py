from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from api.signup.db import create_user

app = FastAPI()

class User(BaseModel):
    email: str
    username: str
    password: str

@app.post("/signup/")
async def signup(user: User):
    success = create_user(user.email, user.username, user.password)
    if not success:
        raise HTTPException(status_code=400, detail="Error creating user")
    return {"message": "your account created successfully."}
