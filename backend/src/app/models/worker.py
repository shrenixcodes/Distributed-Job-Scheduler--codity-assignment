
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
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


class Worker(Base):
    __tablename__ = "workers"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    status = Column(String(50), default="idle")
    last_heartbeat = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WorkerHeartbeat(Base):
    __tablename__ = "worker_heartbeats"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    worker_id = Column(_uuid_type, ForeignKey("workers.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

