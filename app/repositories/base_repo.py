from typing import Any, Type
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder

class BaseRepo:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    async def get_by_id(self, *, session: AsyncSession, id: Any) -> SQLModel | None:
        return await session.get(self.model, id)

    async def get_multi(self, *, session: AsyncSession, skip: int = 0, limit: int = 100) -> list[SQLModel]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await session.exec(statement)
        return result.all()

    async def get_by_field(self, *, session: AsyncSession, field_name: str, value: Any) -> SQLModel | None:
        statement = select(self.model).where(getattr(self.model, field_name) == value)
        result = await session.exec(statement)
        return result.first()

    async def create(self, *, session: AsyncSession, obj_in: dict[str, Any]) -> SQLModel:
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, *, session: AsyncSession, db_obj: SQLModel, obj_in: dict[str, Any]) -> SQLModel:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, SQLModel):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete(self, *, session: AsyncSession, db_obj: SQLModel) -> SQLModel | None:
            await session.delete(db_obj)
            await session.commit()
            return db_obj