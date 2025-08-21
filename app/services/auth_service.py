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

log = structlog.get_logger()

class AuthService:
    def __init__(self):
        self.user_repo = user_repo
        self.session_repo = session_repo

    def _prepare_session_data(self, user_id: int, request: Request) -> dict:
        """Prepares the data dictionary for creating a new session."""
        expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        return {
            "expires_at": datetime.utcnow() + expires_delta,
            "user_id": user_id,
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        }

    async def login(self, *, db: AsyncSession, request: Request, email: str, password: str) -> tuple[str, str]:
        log.info("Login attempt", email=email, request_id=str(request_id_var.get()))
        
        user = await self.user_repo.get_by_email(db=db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        
        session_data = self._prepare_session_data(user_id=user.id, request=request)
        new_session = await self.session_repo.create(db=db, obj_in=session_data)
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email, "jti": str(new_session.id)})
        log.info(
            "Login successful",
            user_id=user.id,
            session_id=new_session.id,
            request_id=request_id
        )
        return access_token, refresh_token

    async def refresh(self, *, db: AsyncSession, request: Request, old_session: SessionModel) -> tuple[str, str]:
        log.info(
            "Token refresh attempt",
            user_id=old_session.user_id,
            session_id=old_session.id,
            request_id=str(request_id_var.get())
        )
        
        await self.session_repo.delete(db=db, db_obj=old_session)

        session_data = self._prepare_session_data(user_id=old_session.user_id, request=request)
        new_session = await self.session_repo.create(db=db, obj_in=session_data)
        access_token = create_access_token(data={"sub": old_session.user.email})
        refresh_token = create_refresh_token(data={"sub": old_session.user.email, "jti": str(new_session.id)})
        log.info(
            "Token refresh successful",
            user_id=new_session.user_id,
            new_session_id=new_session.id,
            request_id=str(request_id_var.get())
        )
        return access_token, refresh_token

    async def logout(self, *, db: AsyncSession, session_to_delete: SessionModel):
        log.info(
            "Logout attempt",
            user_id=session_to_delete.user_id,
            session_id=session_to_delete.id,
            request_id=str(request_id_var.get())
        )
        await self.session_repo.delete(db=db, db_obj=session_to_delete)
        log.info(
            "Logout Successful",
            user_id=session_to_delete.user_id,
            request_id=str(request_id_var.get())
        )

auth_service = AuthService()