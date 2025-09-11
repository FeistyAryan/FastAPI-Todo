from sqlmodel import SQLModel

class ClothingItemCreate(SQLModel):
    description: str
    category: str
    colors: list[str] = []
    fit_type: str | None = None
    formality_level: int = 3

class ClothingItemUpdate(SQLModel):
    description: str | None = None
    category: str | None = None
    colors: list[str] | None = None
    fit_type: str | None = None
    formality_level: int | None = None

class OutfitCreate(SQLModel):
    name: str | None = None
    clothing_items: list[int]
    description: str | None = None

class OutfitUpdate(SQLModel):
    name: str | None = None
    clothing_items: list[int] | None = None
    description: str | None = None
    user_rating: int | None = None

class ShoppingRecommendationCreate(SQLModel):
    item_type: str
    description: str
    reasoning: str
    priority_score: float
    estimated_price_range: str | None = None
    complementary_items: list[int] = []
