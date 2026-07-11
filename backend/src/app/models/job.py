
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from ..core.database import Base

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False, default="queued")
    payload = Column(JSONB, nullable=False)
    priority = Column(Integer, default=0)
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    failed_at = Column(DateTime(timezone=True))
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class JobExecution(Base):
    __tablename__ = "job_executions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(UUID(as_uuid=True), ForeignKey("workers.id", ondelete="SET NULL"))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    status = Column(String(50))
    output = Column(JSONB)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    cron_expression = Column(String(100), nullable=False)
    payload = Column(JSONB, nullable=False)
    next_run_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class DeadLetterQueue(Base):
    __tablename__ = "dead_letter_queue"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    original_job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    payload = Column(JSONB, nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
