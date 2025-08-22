import uuid
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import ValidationError
from typing import Annotated
from datetime import datetime

from app.core.config import settings
from app.db import get_db
from app.repositories.user_repo import user_repo
from app.repositories.session_repo import session_repo
from app.models.user import User
from app.models.session import Session as SessionModel
from app.core.exceptions.user import InvalidCredentialsException
from app.core.exceptions.session import InvalidSessionException
from app.core.jwt_denylist import is_jti_denylisted

# This tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

async def get_current_user(db: Annotated[AsyncSession, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")
        if not jti or await is_jti_denylisted(jti):
            raise InvalidCredentialsException()

        email = payload.get("sub")
    except(JWTError, ValidationError):
        raise InvalidCredentialsException()

    user = await user_repo.get_by_email(db=db, email=email)
    if user is None:
        raise InvalidCredentialsException()

    return user

async def get_valid_session_model_from_refresh_token(db: Annotated[AsyncSession, Depends(get_db)], refresh_token: str = Cookie(...)) -> SessionModel:
    if not refresh_token:
        raise InvalidSessionException()

    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        session_id = payload.get("jti")
        if not session_id:
            raise InvalidSessionException()

    except JWTError:
        raise InvalidSessionException()

    current_session = await session_repo.get_session_with_user(db=db, id=uuid.UUID(session_id))
    if not current_session or current_session.expires_at < datetime.utcnow():
        raise InvalidSessionException()
            
    return current_session