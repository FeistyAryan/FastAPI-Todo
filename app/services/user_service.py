import structlog
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
import secrets
import hashlib

from app.repositories.user_repo import user_repo
from app.repositories.password_reset_token_repo import password_reset_token_repo
from app.schemas.user import UserCreate, ResetPassword
from app.models.user import User
from app.core.context import request_id_var
from app.core.security import get_password_hash
from app.core.exceptions.user import UserAlreadyExistsException, UserNotFoundException
from app.core.config import settings

log = structlog.get_logger()

class UserService:
    def __init__(self):
        self.repo = user_repo
        self.password_reset_token_repo = password_reset_token_repo

    async def register_new_user(self, *, db: AsyncSession, user_in: UserCreate) -> User:      
        user_data = user_in.model_dump(include={"email"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        log.info("Attempting to register new user", email=user_in.email, request_id=str(request_id_var.get()))

        try:
            new_user = await self.repo.create(db=db, obj_in=user_data)
            log.info("New user registered", email=new_user.email, request_id=str(request_id_var.get()))
            return new_user

        except IntegrityError:
            await db.rollback()
            raise UserAlreadyExistsException()

    async def start_password_reset(self, *, db: AsyncSession, email: str):
        log.info("Password reset requested", email=email, request_id=str(request_id_var.get()))
        user = await self.repo.get_by_email(db=db, email=email)
        if not user:
            raise UserNotFoundException()

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        
        token_data = {
            "token_hash": token_hash,
            "expires_at": datetime.utcnow() + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES),
            "user_id": user.id
        }
        await self.password_reset_token_repo.create(db=db, obj_in=token_data)
        return raw_token

    async def reset_password(self, *, db: AsyncSession, payload: ResetPassword):
        token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
        token_obj = await self.password_reset_token_repo.get_by_token_hash(db=db, token_hash=token_hash)
        if not token_obj or token_obj.expires_at < datetime.utcnow():
            raise InvalidCredentialsException(detail="Invalid or expired password reset token.")
        
        user = await self.repo.get_by_id(db=db, id=token_obj.user_id)
        user.hashed_password = get_password_hash(payload.new_password)
        db.add(user)
        await self.password_reset_token_repo.delete_all_for_user(db=db, user_id=user.id)
        await db.commit()
        log.info("Password reset successful", email=user.email, user_id=user.id)
        
user_service = UserService()