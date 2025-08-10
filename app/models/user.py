from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.session import Session

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True

    sessions: list["Session"] = Relationship(back_populates="user")