
from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from ..core.database import Base

class Queue(Base):
    __tablename__ = "queues"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=0)
    concurrency_limit = Column(Integer, default=1)
    is_paused = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class RetryPolicy(Base):
    __tablename__ = "retry_policies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id", ondelete="CASCADE"), nullable=False)
    max_retries = Column(Integer, default=3)
    strategy = Column(String(50), nullable=False, default="fixed")
    delay_seconds = Column(Integer, default=60)
    max_delay_seconds = Column(Integer, default=3600)
    backoff_multiplier = Column(Numeric, default=2.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
