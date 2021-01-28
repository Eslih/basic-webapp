from typing import Union, Any

from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from .. import actions, config
from ..db.session import SessionLocal
from ..schemas import TokenPayload, User

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_VERSION_STR}/auth/access-token"
)


# Dependency to get DB session.
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, config.settings.SECRET_KEY, algorithm='HS256')
    return encoded_jwt


def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    try:
        payload = jwt.decode(token, config.settings.SECRET_KEY, algorithms=['HS256'])
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = actions.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user
