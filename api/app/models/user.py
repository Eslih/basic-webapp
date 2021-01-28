from uuid import uuid4
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ..db import Base


# SQLAlchemy model
class User(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    password = Column(String, nullable=False)
    email = Column(String(80), unique=True, nullable=False, index=True)
    username = Column(String(40), unique=True, nullable=False, index=True)
