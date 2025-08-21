from sqlmodel import SQLModel
from pydantic import EmailStr

class UserCreate(SQLModel):
    email: EmailStr
    password: str

class UserRead(SQLModel):
    id: int
    email: EmailStr
    is_active: bool

class ForgotPassword(SQLModel):
    email: EmailStr