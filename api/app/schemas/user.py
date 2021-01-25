from typing import Optional
from pydantic import BaseModel, UUID4, EmailStr


# https://pydantic-docs.helpmanual.io/
# Data validation and settings management using python type annotations.
# pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid.
# Define how data should be in pure, canonical python; validate it with pydantic.

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    # Don't add username here, otherwise it will be editable (via UserUpdate)


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDBBase(UserBase):
    id: Optional[UUID4] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    # You probably want to return this when a get request is fired.
    username: str


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    password: str
