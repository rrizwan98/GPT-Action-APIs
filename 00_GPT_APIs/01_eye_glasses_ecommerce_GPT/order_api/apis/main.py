# main.py
from fastapi import FastAPI
from apis.routes import router  # make sure the import path matches your project structure

app = FastAPI(
    title = "EYE Classes E-commerce API",
    description = "Order EYE Glasses through GPT. and also recomended eye Glasses",
    version = "0.1"
)
app.include_router(router)
