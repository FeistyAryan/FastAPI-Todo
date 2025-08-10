from fastapi import FastAPI
from app.api.v1.api import api_router

app = FastAPI(title="Production Grade FastAPI")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API is live!"}