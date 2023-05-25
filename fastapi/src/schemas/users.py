from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: Optional[str]
    hashed_password: str


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    hashed_password: Optional[str]


class User(UserBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        orm_mode = True
