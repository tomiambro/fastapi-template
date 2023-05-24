import os
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from settings.config import data

ACCESS_TOKEN_EXPIRE_DAYS = 365  # 1 year
REFRESH_TOKEN_EXPIRE_DAYS = 30 * 3  # 3 months
ALGORITHM = "HS256"
JWT_SECRET_KEY = data["jwt_secret"]
JWT_REFRESH_SECRET_KEY = data["jwt_secret"]


def create_access_token(subject: Union[str, Any], expires_delta: int = 30) -> str:
    if expires_delta is not None:
        delta = datetime.utcnow() + timedelta(days=expires_delta)
    else:
        delta = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    to_encode = {"exp": delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt
