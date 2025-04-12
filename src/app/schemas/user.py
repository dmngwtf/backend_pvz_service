from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"