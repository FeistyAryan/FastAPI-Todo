# in app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.api import api_router
from app.core.exceptions.base import CustomException
from app.core.exceptions.handlers import custom_exception_handler, generic_exception_handler
from app.core.middlewares.correlation import CorrelationIDMiddleware
from app.core.logging_config import setup_logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(title="Production Grade FastAPI", lifespan=lifespan)

Instrumentator().instrument(app).expose(app)

app.add_middleware(CorrelationIDMiddleware)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "API is live!"}