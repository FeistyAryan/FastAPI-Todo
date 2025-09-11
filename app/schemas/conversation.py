from sqlmodel import SQLModel

class ConversationCreate(SQLModel):
    chat_name: str
    input_data: dict
    recommendations: dict = {}