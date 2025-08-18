from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

from app.models.base import TimestampModel

if TYPE_CHECKING:
    from app.models.session import Session

class User(TimestampModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True

    sessions: list["Session"] = Relationship(back_populates="user")