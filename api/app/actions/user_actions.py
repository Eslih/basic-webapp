from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ..actions.base import BaseActions
from ..models import User
from ..schemas import UserCreate, UserUpdate
from ..security import get_password_hash, verify_password


class UserActions(BaseActions[User, UserCreate, UserUpdate]):
    """User actions with basic CRUD operations"""

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            password=get_password_hash(obj_in.password),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, *, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_username_or_email(self, db: Session, *, username: str, email: EmailStr) -> Optional[User]:
        return db.query(User).filter(or_(User.email == email, User.username == username)).first()

    def update(
            self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        update_data = obj_in.dict(exclude_unset=True)
        if update_data['password']:
            update_data['password'] = get_password_hash(update_data['password'])
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user = UserActions(User)
