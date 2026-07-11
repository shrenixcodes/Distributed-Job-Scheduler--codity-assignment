
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class WorkerResponse(BaseModel):
    id: UUID
    name: str
    status: str
    last_heartbeat: datetime | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
