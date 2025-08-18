from fastapi import HTTPException, status, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime, timedelta

from app.repositories.user_repo import user_repo
from app.repositories.session_repo import session_repo
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.models.session import Session as SessionModel

class AuthService:
    def __init__(self):
        self.user_repo = user_repo
        self.session_repo = session_repo

    async def login(self, *, session: AsyncSession, request: Request, email: str, password: str) -> tuple[str, str]:
        user = await self.user_repo.get_by_email(session=session, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        session_data = {
            "expires_at": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            "user_id": user.id,
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        }
        db_session = await self.session_repo.create(session=session, obj_in=session_data)
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email, "jti": str(db_session.id)})
        return access_token, refresh_token

    async def refresh(self, *, session: AsyncSession, request: Request, old_session: SessionModel) -> tuple[str, str]:
        await self.session_repo.delete(session=session, db_obj=old_session)

        session_data = {
            "expires_at": datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
            "user_id": old_session.user_id,
            "user_agent": request.headers.get("user-agent"),
            "ip_address": request.client.host
        }
        new_db_session = await self.session_repo.create(session=session, obj_in=session_data)
        access_token = create_access_token(data={"sub": old_session.user.email})
        refresh_token = create_refresh_token(data={"sub": old_session.user.email, "jti": str(new_db_session.id)})
        return access_token, refresh_token

    async def logout(self, *, session: AsyncSession, session_to_delete: SessionModel):
        await self.session_repo.delete(session=session, db_obj=session_to_delete)

auth_service = AuthService()