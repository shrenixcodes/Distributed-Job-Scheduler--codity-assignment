
import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.sql import func
from ..core.database import Base

# Use database-agnostic UUID column
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


class User(Base):
    __tablename__ = "users"
    
    id = Column(_uuid_type, primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

