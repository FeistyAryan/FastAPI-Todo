from sqlmodel import SQLModel, Field
from datetime import datetime

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None, sa_column_kwargs={"onupdate": datetime.utcnow})