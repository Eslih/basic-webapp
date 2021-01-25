from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)

# https://docs.sqlalchemy.org/en/13/orm/session_basics.html
# Connection pooling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
