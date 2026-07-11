
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    # The API derives the organization from the authenticated user unless an
    # organization is explicitly supplied and the user belongs to it.
    organization_id: UUID | None = None

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    organization_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
