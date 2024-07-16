# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as product_router

app = FastAPI(
    title = "Product API",
    description = "A simple API to perform CRUD operations on products.",
    servers = [{"url": "https://adminapi.blackflower-9e2d4f52.eastus2.azurecontainerapps.io/", "description": "Deploy Admin api in Azure Container APP"}],
    version = "0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(product_router)
