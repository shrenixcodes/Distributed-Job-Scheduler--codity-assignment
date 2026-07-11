
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    organization_id: UUID

class ProjectResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    organization_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
