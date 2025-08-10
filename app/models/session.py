import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.model.user import User

class Session(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime
    user_id: int = Field(foreign_key='user.id')
    user_agent: str = Field(default=None)
    ip_address: str = Field(default=None)

    user: "User" = Relationship(back_populates="sessions")