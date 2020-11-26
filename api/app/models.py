import os

from sqlalchemy import (Column, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

pg_user = os.getenv('PG_USER', 'postgres')
pg_host = os.getenv('PG_HOST', 'localhost')
pg_port = os.getenv('PG_PORT', '5432')
pg_database = os.getenv('PG_DATABASE', 'postgres')
pg_password = os.getenv('PG_PASSWORD', 'postgres_password')

engine = create_engine(
    'postgresql://' + pg_user + ':' + pg_password + '@' + pg_host + ':' + pg_port + '/' + pg_database
)
session = sessionmaker(autoflush=False, bind=engine)  # autocommit=False,
db = session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def delete_users():
        try:
            num_rows_deleted = db.query(User).delete()
            db.commit()
            return num_rows_deleted
        except Exception:
            db.rollback()


Base.metadata.create_all(engine)
