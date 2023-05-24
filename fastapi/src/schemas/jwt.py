from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JWTBase(BaseModel):
    token: str
    expiration_date: datetime = datetime.now()
    wordpress_id: int

    def __str__(self):
        return f"<schemas.JWTBase(token='{self.token}', expiration_date={self.expiration_date}, wordpress_id={self.wordpress_id})>"


class JWTCreate(JWTBase):
    def __str__(self):
        return f"<schemas.JWTCreate(token='{self.token}', exp_date={self.expiration_date})>"


class JWTUpdate(BaseModel):
    token: Optional[str]
    expiration_date: Optional[datetime] = datetime.now()
    wordpress_id: Optional[int]

    def __str__(self):
        return f"<schemas.JWTUpdate(token='{self.token}', expiration_date={self.expiration_date}, wordpress_id={self.wordpress_id})>"


class JWT(JWTBase):
    id: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        orm_mode = True

    def __str__(self):
        return (
            f"<schemas.JWT(id={self.id}, token='{self.token}', expiration_date={self.expiration_date}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
