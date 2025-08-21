import structlog
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.context import request_id_var
from app.core.security import get_password_hash
from app.core.exceptions.user import UserAlreadyExistsException

log = structlog.get_logger()

class UserService:
    def __init__(self):
        self.repo = user_repo

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

user_service = UserService()