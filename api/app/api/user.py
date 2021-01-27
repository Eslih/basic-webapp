from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_401_UNAUTHORIZED

from .dependencies import get_db, get_current_user
from .. import actions
from ..schemas import User, UserCreate, HTTPError, UserUpdate

user_router = APIRouter()


@user_router.get("/", response_model=List[User], tags=["users"])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), skip: int = 0,
               limit: int = 100) -> Any:
    users = actions.user.get_all(db=db, skip=skip, limit=limit)
    return users


@user_router.post(
    "/create", response_model=User, status_code=HTTP_201_CREATED, tags=["users"]
)
def create_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    user = actions.user.get_by_username_or_email(db, email=user_in.email, username=user_in.username)
    if user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail="A user with this email or username already exists.")
    user = actions.user.create(db=db, obj_in=user_in)
    return user


@user_router.put(
    "/edit/{id}",
    response_model=User,
    responses={HTTP_404_NOT_FOUND: {"model": HTTPError}},
    tags=["users"],
)
def update_user(
        *, db: Session = Depends(get_db), id: UUID4, user_in: UserUpdate,
) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    user = actions.user.update(db=db, db_obj=user, obj_in=user_in)
    return user


@user_router.get(
    "/{id}",
    response_model=User,
    responses={HTTP_404_NOT_FOUND: {"model": HTTPError}},
    tags=["users"],
)
def get_user(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user


@user_router.delete(
    "/delete/{id}",
    response_model=User,
    responses={HTTP_404_NOT_FOUND: {"model": HTTPError}},
    tags=["users"],
)
def delete_user(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), id: UUID4) -> Any:
    user = actions.user.get(db=db, id=id)
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    user = actions.user.remove(db=db, id=id)
    return user


@user_router.delete(
    "/delete",
    response_model=int,
    responses={HTTP_401_UNAUTHORIZED: {"model": HTTPError}},
    tags=["users"],
)
def delete_users(*, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Any:
    return actions.user.remove_al(db=db)
