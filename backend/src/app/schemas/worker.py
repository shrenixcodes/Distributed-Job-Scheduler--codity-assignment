
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class WorkerResponse(BaseModel):
    id: UUID
    name: str
    status: str
    last_heartbeat: datetime | None = None
    created_at: datetime

    class Config:
        from_attributes = True
