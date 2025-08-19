from fastapi import FastAPI
from app.api.v1.api import api_router
from app.core.exceptions.base import CustomException
from app.core.exceptions.handlers import custom_exception_handler

app = FastAPI(title="Production Grade FastAPI")

app.add_exception_handler(CustomException, custom_exception_handler)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API is live!"}