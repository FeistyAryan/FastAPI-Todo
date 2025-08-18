import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.session import Session as SessionModel
from app.repositories.base_repo import BaseRepo

class SessionRepo(BaseRepo):
    def __init__(self):
        super().__init__(SessionModel)

    async def get_session_with_user(self, *, session: AsyncSession, id: uuid.UUID) -> SessionModel | None:
        statement = select(self.model).where(self.model.id==id).options(selectinload(self.model.user))
        result = await session.exec(statement)
        return result.one_or_none()

session_repo = SessionRepo()