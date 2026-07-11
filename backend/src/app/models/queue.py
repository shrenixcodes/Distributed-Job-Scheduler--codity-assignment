
import uuid
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, ForeignKey, Numeric
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


class Queue(Base):
    __tablename__ = "queues"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    project_id = Column(_uuid_type, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=0)
    concurrency_limit = Column(Integer, default=1)
    is_paused = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class RetryPolicy(Base):
    __tablename__ = "retry_policies"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    queue_id = Column(_uuid_type, ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    max_retries = Column(Integer, default=3)
    strategy = Column(String(50), nullable=False, default="fixed")
    delay_seconds = Column(Integer, default=60)
    max_delay_seconds = Column(Integer, default=3600)
    backoff_multiplier = Column(Numeric, default=2.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

