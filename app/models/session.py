import uuid
from sqlmodel import Field, Relationship
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from app.models.base import TimestampModel

if TYPE_CHECKING:
    from app.model.user import User

class Session(TimestampModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    expires_at: datetime
    user_id: int = Field(foreign_key='user.id')
    user_agent: str = Field(default=None)
    ip_address: str = Field(default=None)

    user: "User" = Relationship(back_populates="sessions")