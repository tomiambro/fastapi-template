from datetime import datetime
from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import ValidationError
from settings import logger_for
from utilities.jwt_token import ALGORITHM, JWT_SECRET_KEY

logger = logger_for(__name__)

from fastapi import HTTPException, status


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
    authorization: str = request.headers.get("Authorization")
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
