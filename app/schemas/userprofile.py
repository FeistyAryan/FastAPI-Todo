from sqlmodel import SQLModel

class UserStylistProfileUpdate(SQLModel):
    body_type: str | None = None
    skin_tone: str | None = None
    style_preferences: dict | None = None
    budget_range: str | None = None
    lifestyle: str | None = None
    sizing_info: dict | None = None