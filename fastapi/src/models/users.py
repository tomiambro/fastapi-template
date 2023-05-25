import sqlalchemy

from .base_class import BaseClass


class User(BaseClass):
    __tablename__ = "users"
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(100), nullable=False, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
