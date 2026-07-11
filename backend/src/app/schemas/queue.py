
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class QueueCreate(BaseModel):
    name: str
    description: str | None = None
    project_id: UUID
    priority: int = 0
    concurrency_limit: int = 1

class RetryPolicyCreate(BaseModel):
    queue_id: UUID
    max_retries: int = 3
    strategy: str = "fixed"
    delay_seconds: int = 60
    max_delay_seconds: int = 3600
    backoff_multiplier: float = 2.0

class QueueResponse(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    project_id: UUID
    priority: int
    concurrency_limit: int
    is_paused: bool
    created_at: datetime

    class Config:
        from_attributes = True
