from datetime import datetime
from typing import Optional

from dao import user_dao
from db import conn
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from schemas import User
from settings import logger_for
from sqlalchemy.orm import Session
from utilities.jwt_token import ALGORITHM, JWT_SECRET_KEY

from fastapi import Depends, HTTPException, Request, status

logger = logger_for(__name__)

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="users/login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(reuseable_oauth), db: Session = Depends(conn)
) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_dao.get_by_field(db, "email", payload["sub"])

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])

        if datetime.fromtimestamp(payload["exp"]) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def token_in_header(request: Request) -> str:
    authorization: Optional[str] = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid scheme"
        )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Token not found"
        )

    return token
