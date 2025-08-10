import uuid
from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import ValidationError
from typing import Annotated
from datetime import datetime

from app.core.config import settings
from app.db import get_session
from app.crud.user import get_user_by_email
from app.crud.session import get_session_by_id
from app.models.user import User
from app.models.session import Session as SessionModel
from app.schemas.token import TokenData

# This tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")

async def get_current_user(session: Annotated[AsyncSession, Depends(get_session)], token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(email=payload.get("sub"))
    except(JWTError, ValidationError):
        raise credential_exception

    user = await get_user_by_email(session=session, email=token_data.email)
    if user is None:
        raise credential_exception

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")

    return user

async def get_valid_session_model_from_refresh_token(session: Annotated[AsyncSession, Depends(get_session)], refresh_token: str = Cookie(...)) -> SessionModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, please log in again",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not refresh_token:
        raise credentials_exception

    try:
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        session_id = payload.get("jti")
        if not session_id:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    db_session = await get_session_by_id(session=session, id=uuid.UUID(session_id))
    print("this is the db_session", db_session)
    if not db_session or db_session.expires_at < datetime.utcnow():
        raise credentials_exception
            
    return db_session