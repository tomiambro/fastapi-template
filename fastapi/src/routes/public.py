from typing import Dict

import schemas
from constants import DEVELOPMENT
from dao import jwt_dao, wordpress_dao
from db import conn
from jose import jwt
from settings import logger_for
from settings.config import data
from sqlalchemy.orm import Session
from utilities.jwt_token import ALGORITHM, JWT_SECRET_KEY, create_access_token

from fastapi import APIRouter, Depends, HTTPException

from .deps import decode_token

logger = logger_for(__name__)

router = APIRouter(prefix="/api/v1/public")


@router.get("/current_token", summary="Get the current token", response_model=Dict)
def get_current_token(token: Dict = Depends(decode_token)):
    return token


@router.post("/token/{hash_value}")
def token(hash_value: str, db: Session = Depends(conn)):
    # This endpoint is for testing purposes.
    #
    # It creates a new token associating it the provided URL. This blog must
    # already exist in the database. If it doesn't use the `/wordpress_installation` route below
    #
    # And saves the token to the db.
    if data["env"] == DEVELOPMENT:
        # Update this URL; it is what will be encoded in the JWT
        url = "https://bullpen-wp.clone.network"

        if hash_value == data["hash_value"]:
            blog = wordpress_dao.get_by_field(db, "blog_url", url)
            token = {
                "access_token": create_access_token(url),
            }
            payload = jwt.decode(
                token["access_token"], JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )
            token_data = {
                "token": token["access_token"],
                "expiration_date": payload["exp"],
                "wordpress_id": blog.id,
            }
            jwt_dao.create(db, schemas.JWTCreate(**token_data))
            return token
        else:
            raise HTTPException(status_code=401, detail="Incorrect hash value provided")
    raise HTTPException(status_code=404)


@router.post("/wordpress_installation")
def wordpress_registration(data: schemas.WordpressCreate, db: Session = Depends(conn)):
    blog_exists = wordpress_dao.get_by_field(db, field="blog_url", value=data.blog_url)

    if blog_exists is None:
        record = wordpress_dao.create(db, data)

        # Generate JWT and return it to the user
        token = {
            "access_token": create_access_token(record.blog_url),
        }
        payload = jwt.decode(
            token["access_token"], JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = {
            "token": token["access_token"],
            "expiration_date": payload["exp"],
            "wordpress_id": record.id,
        }
        jwt_dao.create(db, schemas.JWTCreate(**token_data))

        return {"message": "Blog registered", "token": token["access_token"]}

    if blog_exists and blog_exists.active == False:
        blog_exists.blog_name = data.blog_name
        blog_exists.blog_url = data.blog_url
        blog_exists.blog_description = data.blog_description
        blog_exists.db_version = data.db_version
        blog_exists.user_email = data.user_email
        blog_exists.site_version = data.site_version
        blog_exists.api_credentials = data.api_credentials
        blog_exists.save(db)

        # Generate JWT and return it to the user
        token = {
            "access_token": create_access_token(blog_exists.blog_url),
        }
        payload = jwt.decode(
            token["access_token"], JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = {
            "token": token["access_token"],
            "expiration_date": payload["exp"],
            "wordpress_id": blog_exists.id,
        }
        jwt_dao.create(db, schemas.JWTCreate(**token_data))

        return {"message": "Blog updated", "token": token["access_token"]}
    if blog_exists and blog_exists.active == True:
        raise HTTPException(status_code=401, detail="Blog already registered")
