import uuid
from datetime import datetime, timedelta
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.session import Session as SessionModel
from app.core.config import settings

async def create_session(*, session: AsyncSession, user_id: int, user_agent: str, ip_address: str ) -> SessionModel:
    expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    expires_at = datetime.utcnow() + expires_delta

    db_session = SessionModel(
        expires_at=expires_at,
        user_id=user_id, 
        user_agent=user_agent, 
        ip_address=ip_address
    )
    session.add(db_session)
    await session.commit()
    await session.refresh(db_session)
    return db_session

async def get_session_by_id(*, session: AsyncSession, id: uuid.UUID) -> SessionModel:
    statement = select(SessionModel).where(SessionModel.id==id).options(selectinload(SessionModel.user))
    result = await session.exec(statement)
    return result.one_or_none()

async def delete_session_by_id(*, session: AsyncSession, id: uuid.UUID):
    db_session = await get_session_by_id(session=session, id=id)
    if db_session:
        await session.delete(db_session)
        await session.commit()