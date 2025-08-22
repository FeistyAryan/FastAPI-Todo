import structlog
from fastapi import HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta

from app.repositories.user_repo import user_repo
from app.repositories.session_repo import session_repo
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.core.context import request_id_var
from app.models.session import Session as SessionModel
from app.core.exceptions.user import InvalidCredentialsException
from app.core.jwt_denylist import add_jti_to_denylist

log = structlog.get_logger()

class AuthService:
    def __init__(self):
        self.user_repo = user_repo
        self.session_repo = session_repo

    async def generate_tokens_with_session(self, *, db: AsyncSession, user_id: int, email: str, request: Request) -> tuple[str, str, SessionModel]:
        """Prepares the data dictionary for creating a new session."""
        expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        session_data = {
            "expires_at": datetime.utcnow() + expires_delta,
            "user_id": user_id,
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        }
        new_session = await self.session_repo.create(db=db, obj_in=session_data)
        jti = str(new_session.id)
        access_token = create_access_token(data={"sub": email, "jti": jti})
        refresh_token = create_refresh_token(data={"sub": email, "jti": jti})
        return access_token, refresh_token, new_session

    async def login(self, *, db: AsyncSession, request: Request, email: str, password: str) -> tuple[str, str]:
        log.info("Login attempt", email=email, request_id=str(request_id_var.get()))
        
        user = await self.user_repo.get_by_email(db=db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        
        access_token, refresh_token, new_session = await self.generate_tokens_with_session(db=db, user_id=user.id, email=user.email, request=request)
        log.info(
            "Login successful",
            email=email,
            session_id=new_session.id,
            request_id=str(request_id_var.get())
        )
        return access_token, refresh_token

    async def refresh(self, *, db: AsyncSession, request: Request, old_session: SessionModel) -> tuple[str, str]:
        log.info(
            "Token refresh attempt",
            email=old_session.user.email,
            session_id=old_session.id,
            request_id=str(request_id_var.get())
        )
        
        await self.session_repo.delete(db=db, db_obj=old_session)

        access_token, refresh_token, new_session = await self.generate_tokens_with_session(db=db, user_id=old_session.user_id, email=old_session.user.email, request=request)
        log.info(
            "Token refresh successful",
            email=new_session.user.email,
            new_session_id=new_session.id,
            request_id=str(request_id_var.get())
        )
        return access_token, refresh_token

    async def logout(self, *, db: AsyncSession, session_to_delete: SessionModel, access_token: str):
        log.info(
            "Logout attempt",
            email=session_to_delete.user.email,
            session_id=session_to_delete.id,
            request_id=str(request_id_var.get())
        )
        try:
            payload = jwt.decode(access_token, settings.ACCESS_SECRET_KEY, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            exp = payload.get("exp")
            if jti and exp:
                await add_jti_to_denylist(jti, exp)
        except JWTError:
            log.warn("Invalid access token provided during logout", request_id=str(request_id_var.get()))

        await self.session_repo.delete(db=db, db_obj=session_to_delete)
        log.info(
            "Logout Successful",
            email=session_to_delete.user.email,
            request_id=str(request_id_var.get())
        )

auth_service = AuthService()