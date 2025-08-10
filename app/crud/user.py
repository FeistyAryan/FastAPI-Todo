from sqlmodel import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession

async def create_user(*, session:AsyncSession, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_password)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

async def get_user_by_email(*, session:AsyncSession, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    user = await session.exec(statement)
    return user.first()