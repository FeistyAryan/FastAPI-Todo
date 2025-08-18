from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated

from app.api.v1.dependencies import get_current_user
from app.db import get_session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.services.user_service import user_service

router = APIRouter()

@router.post("/register",
response_model=UserRead
)
async def register_user(
    *,
    session: Annotated[AsyncSession, Depends(get_session)],
    user_in: UserCreate
):

    return await user_service.register_new_user(session=session, user_in=user_in)
    

@router.get("/me",
response_model=UserRead 
)
async def read_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user