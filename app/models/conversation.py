from sqlmodel import Field, Relationship, JSON, Column
from typing import TYPE_CHECKING


from app.models.base import TimestampModel
from app.core.enums import MessageRole

if TYPE_CHECKING:
    from app.models.user import User

class Conversation(TimestampModel, table=True):
    """Model representing the chat room or session header"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    chat_name: str

    # Relationships
    messages: list["ConversationMessage"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")


class ConversationMessage(TimestampModel, table=True):
    """Model representing a single message within a conversation"""

    __tablename__ = "conversation_message"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id")
    role: MessageRole
    content: dict = Field(sa_column=Column(JSON))

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")