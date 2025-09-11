from sqlmodel import Field, Relationship, SQLModel, JSON, Column
from typing import TYPE_CHECKING, Any

from app.models.base import TimestampModel

if TYPE_CHECKING:
    from app.models.session import Session
    from app.models.password_reset_token import PasswordResetToken
    from app.models.wardrobe import ClothingItem, Outfit, ShoppingRecommendation
    from app.models.conversation import Conversation

class User(TimestampModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    is_active: bool = True
    
    # AI Stylist related fields
    body_type: str | None = Field(default=None)
    skin_tone: str | None = Field(default=None)
    style_preferences: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))
    budget_range: str | None = Field(default=None)
    lifestyle: str | None = Field(default=None)
    sizing_info: dict[str, Any] | None = Field(default=None, sa_column=Column(JSON))

    # Relationships
    sessions: list["Session"] = Relationship(back_populates="user")
    password_reset_tokens: list["PasswordResetToken"] = Relationship(back_populates="user")
    clothing_items: list["ClothingItem"] = Relationship(back_populates="user")
    outfits: list["Outfit"] = Relationship(back_populates="user")
    shopping_recommendations: list["ShoppingRecommendation"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")