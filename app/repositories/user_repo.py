from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.base_repo import BaseRepo
from app.models.user import User


class UserRepo(BaseRepo):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, *, db:AsyncSession, email: str) -> User | None:
        return await self.get_by_field(db=db, field_name="email", value=email)

user_repo = UserRepo()