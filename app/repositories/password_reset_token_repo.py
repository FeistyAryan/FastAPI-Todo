from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, delete

from app.repositories.base_repo import BaseRepo
from app.models.password_reset_token import PasswordResetToken

class PasswordResetTokenRepo(BaseRepo):
    def __init__(self):
        super().__init__(PasswordResetToken)

    async def get_by_token_hash(self, *, db: AsyncSession, token_hash: str):
        return await self.get_by_field(db=db, field_name="token_hash", value=token_hash)

    async def delete_all_for_user(self, *, db: AsyncSession, user_id=int):
        statement = delete(self.model).where(self.model.user_id==user_id)
        await db.exec(statement)

password_reset_token_repo = PasswordResetTokenRepo()