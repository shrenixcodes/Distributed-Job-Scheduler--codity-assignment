
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

class QueueCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    project_id: UUID
    priority: int = Field(default=0, ge=0, le=100)
    concurrency_limit: int = Field(default=1, ge=1, le=100)

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
