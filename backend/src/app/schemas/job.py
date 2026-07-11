
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from typing import Any

class JobCreate(BaseModel):
    queue_id: UUID
    payload: Any
    priority: int = 0
    scheduled_at: datetime | None = None

class ScheduledJobCreate(BaseModel):
    queue_id: UUID
    name: str | None = None
    cron_expression: str
    payload: Any

class JobResponse(BaseModel):
    id: UUID
    queue_id: UUID
    status: str
    payload: Any
    priority: int
    scheduled_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    failed_at: datetime | None = None
    retry_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobExecutionResponse(BaseModel):
    id: UUID
    job_id: UUID
    worker_id: UUID | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: str | None = None
    output: Any | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
