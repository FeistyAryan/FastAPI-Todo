import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

from app.models.base import TimestampModel

if TYPE_CHECKING:
    from app.models.user import User

class PasswordResetToken(TimestampModel, table=True):
    __tablename__ = "password_reset_token"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    token_hash: str = Field(unique=True, index=True)
    expires_at: datetime
    user_id: int = Field(foreign_key="user.id")

    user: "User" = Relationship(back_populates="password_reset_tokens")