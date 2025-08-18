from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_repo import user_repo
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import get_password_hash

class UserService:
    def __init__(self):
        self.repo = user_repo

    async def register_new_user(self, *, session: AsyncSession, user_in: UserCreate) -> User:
        existing_user = await self.repo.get_by_email(session=session, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email already exists."
            )
        
        user_data = user_in.model_dump(include={"email"})
        user_data["hashed_password"] = get_password_hash(user_in.password)

        return await self.repo.create(session=session, obj_in=user_data)

user_service = UserService()