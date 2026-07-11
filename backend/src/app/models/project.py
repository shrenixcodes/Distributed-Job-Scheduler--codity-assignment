
import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
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


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    organization_id = Column(_uuid_type, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

