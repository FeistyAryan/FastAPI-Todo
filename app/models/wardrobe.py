from sqlmodel import Field, Relationship, JSON, Column
from typing import TYPE_CHECKING

from app.models.base import TimestampModel

if TYPE_CHECKING:
    from app.models.user import User


class ClothingItem(TimestampModel, table=True):
    """Model representing a single clothing item in a user's wardrobe"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    description: str = Field(description="description of the clothing item")
    category: str = Field(description="Main category (shirt, pants, dress, shoes, etc.)")
    colors: list[str] = Field(sa_column=Column(JSON), default_factory=list)
    fit_type: str | None = Field(default=None, description="Fit type (slim, regular, loose, etc.)")
    formality_level: int = Field(default=3, description="Formality level on 1-5 scale")
    image_url: str | None = Field(default=None, description="URL to stored image of the item")

    # Relationships
    user: "User" = Relationship(back_populates="clothing_items")


class Outfit(TimestampModel, table=True):
    """Model representing a complete outfit combination"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    name: str | None = Field(default=None, description="User-given name for the outfit")
    clothing_items: list[int] = Field(sa_column=Column(JSON), default_factory=list)
    description: str | None = Field(default=None, description="occasion, weather, season, vibe, etc")
    user_rating: int | None = Field(default=None, description="User rating (1-5 stars)")

    # Relationships
    user: "User" = Relationship(back_populates="outfits")


class ShoppingRecommendation(TimestampModel, table=True):
    """Model representing a shopping recommendation for the user"""

    __tablename__ = "shopping_recommendation"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

    item_type: str = Field(description="Type of item to purchase")
    description: str = Field(description="Detailed description of the recommended item")
    reasoning: str = Field(description="AI reasoning for why this item is recommended")
    priority_score: float = Field(description="Priority score (0.0-1.0) for this recommendation")
    estimated_price_range: str | None = Field(default=None)
    complementary_items: list[int] = Field(sa_column=Column(JSON), default_factory=list)
    purchased: bool = Field(default=False)

    # Relationships
    user: "User" = Relationship(back_populates="shopping_recommendations")