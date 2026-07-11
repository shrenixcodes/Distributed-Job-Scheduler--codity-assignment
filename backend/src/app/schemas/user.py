
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str
