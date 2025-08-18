from typing import Any, Type
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.encoders import jsonable_encoder

class BaseRepo:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    async def get_by_id(self, *, db: AsyncSession, id: Any) -> SQLModel | None:
        return await db.get(self.model, id)

    async def get_multi(self, *, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[SQLModel]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await db.exec(statement)
        return result.all()

    async def get_by_field(self, *, db: AsyncSession, field_name: str, value: Any) -> SQLModel | None:
        statement = select(self.model).where(getattr(self.model, field_name) == value)
        result = await db.exec(statement)
        return result.first()

    async def create(self, *, db: AsyncSession, obj_in: dict[str, Any]) -> SQLModel:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, *, db: AsyncSession, db_obj: SQLModel, obj_in: dict[str, Any]) -> SQLModel:
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, SQLModel):
            update_data = obj_in.dict(exclude_unset=True)
        else:
            update_data = obj_in

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, *, db: AsyncSession, db_obj: SQLModel) -> SQLModel | None:
            await db.delete(db_obj)
            await db.commit()
            return db_obj