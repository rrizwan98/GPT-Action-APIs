# main.py
from fastapi import FastAPI
from apis.routes import router  # make sure the import path matches your project structure

app = FastAPI()

app.include_router(router)
