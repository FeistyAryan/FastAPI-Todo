from fastapi import HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta

from app.repositories.user_repo import user_repo
from app.repositories.session_repo import session_repo
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.models.session import Session as SessionModel
from app.core.exceptions.user import InvalidCredentialsException

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
        user = await self.user_repo.get_by_email(db=db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException()
        
        session_data = self._prepare_session_data(user_id=user.id, request=request)
        new_session = await self.session_repo.create(db=db, obj_in=session_data)
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email, "jti": str(new_session.id)})
        return access_token, refresh_token

    async def refresh(self, *, db: AsyncSession, request: Request, old_session: SessionModel) -> tuple[str, str]:
        await self.session_repo.delete(db=db, db_obj=old_session)

        session_data = self._prepare_session_data(user_id=old_session.user_id, request=request)
        new_session = await self.session_repo.create(db=db, obj_in=session_data)
        access_token = create_access_token(data={"sub": old_session.user.email})
        refresh_token = create_refresh_token(data={"sub": old_session.user.email, "jti": str(new_session.id)})
        return access_token, refresh_token

    async def logout(self, *, db: AsyncSession, session_to_delete: SessionModel):
        await self.session_repo.delete(db=db, db_obj=session_to_delete)

auth_service = AuthService()