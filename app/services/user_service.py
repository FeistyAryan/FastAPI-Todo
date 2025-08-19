from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash
from app.core.exceptions.user import UserAlreadyExistsException

class UserService:
    def __init__(self):
        self.repo = user_repo

    async def register_new_user(self, *, db: AsyncSession, user_in: UserCreate) -> User:
        existing_user = await self.repo.get_by_email(db=db, email=user_in.email)
        if existing_user:
            raise UserAlreadyExistsException()
        
        user_data = user_in.model_dump(include={"email"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        return await self.repo.create(db=db, obj_in=user_data)

user_service = UserService()