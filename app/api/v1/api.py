from fastapi import APIRouter
from app.api.v1.endpoints import user,login

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(login.router, prefix="/auth", tags=["auth"])