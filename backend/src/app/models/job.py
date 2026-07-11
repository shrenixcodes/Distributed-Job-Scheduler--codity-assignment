
import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from ..core.database import Base

try:
    from sqlalchemy import UUID
    _uuid_type = UUID(as_uuid=True)
except ImportError:
    from sqlalchemy.types import TypeDecorator, CHAR
    class UUID(TypeDecorator):
        impl = CHAR
        cache_ok = True
        def __init__(self):
            TypeDecorator.__init__(self, 36)
        def process_bind_param(self, value, dialect):
            if value is None:
                return value
            return str(value)
        def process_result_value(self, value, dialect):
            if value is None:
                return value
            return uuid.UUID(value)
    _uuid_type = UUID()

# Use JSON for SQLite compatibility, JSONB for PostgreSQL
from sqlalchemy import JSON
_json_type = JSON()


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    queue_id = Column(_uuid_type, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False, default="queued")
    payload = Column(_json_type, nullable=False)
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
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    job_id = Column(_uuid_type, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    worker_id = Column(_uuid_type, ForeignKey("workers.id", ondelete="SET NULL"))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    status = Column(String(50))
    output = Column(_json_type)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    queue_id = Column(_uuid_type, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255))
    cron_expression = Column(String(100), nullable=False)
    payload = Column(_json_type, nullable=False)
    next_run_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DeadLetterQueue(Base):
    __tablename__ = "dead_letter_queue"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    original_job_id = Column(_uuid_type, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    queue_id = Column(_uuid_type, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    payload = Column(_json_type, nullable=False)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

