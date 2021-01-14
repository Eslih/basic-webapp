import os

from sqlalchemy import (Column, Integer, String, Binary,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from glob import glob

# Overwrite env vars with a secret if available
for var in glob('/run/secrets/*'):
    k = var.split('/')[-1].upper()
    v = open(var).read().rstrip('\n')
    os.environ[k] = v
    # print(f'export {k}={v}')

pg_user = os.getenv('PG_USER', 'postgres')
pg_host = os.getenv('PG_HOST', 'localhost')
pg_port = os.getenv('PG_PORT', '5432')
pg_database = os.getenv('PG_DATABASE', 'postgres')
pg_password = os.getenv('PG_PASSWORD', 'password')

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
    password = Column(Binary, nullable=False)
    email = Column(String(80), unique=True, nullable=False)

    def __init__(self, username, email, password, id=None):
        self.username = username
        self.email = email
        self.password = password
        self.id = id

    def __repr__(self):
        return f'<User #{self.id}:{self.username}>'

    def delete_users():
        try:
            num_rows_deleted = db.query(User).delete()
            db.commit()
            return num_rows_deleted
        except Exception:
            db.rollback()


Base.metadata.create_all(engine)
