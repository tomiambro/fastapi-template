from typing import Dict

import requests
import schemas
from constants import TEST_ROUTE
from dao import wordpress_dao
from db import conn
from requests.auth import HTTPBasicAuth
from settings import logger_for
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from .deps import decode_token, token_in_header

logger = logger_for(__name__)

router = APIRouter(prefix="/api/v1")


@router.get("/wordpress/{record_id}")
def retrieve(
    record_id: int,
    db: Session = Depends(conn),
    token: str = Depends(token_in_header),
):
    decoded = decode_token(token)
    try:
        record = wordpress_dao.get(db, id=record_id)
        if record is not None:
            # TODO: Turn this into middleware
            if record.blog_url != decoded["sub"]:
                raise HTTPException(
                    status_code=401,
                    detail=f"Invalid token",
                )

            logger.info(record.blog_name)
            return {"message": "Retrieved record!", "record": record}
        else:
            return {
                "message": f"We were unable to find a wordpress record with the id {record_id}"
            }
    except Exception as e:
        logger.error(e)


@router.patch("/wordpress/{record_id}")
def editor(
    record_id: int,
    data: schemas.WordpressUpdate,
    db: Session = Depends(conn),
    token: str = Depends(token_in_header),
):
    decoded = decode_token(token)
    record = wordpress_dao.get_by_field(db, field="id", value=record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"We were unable to find a record with the id {record_id}",
        )

    # TODO: Turn this into middleware
    if record.blog_url != decoded["sub"]:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token",
        )
    updated_record = wordpress_dao.update(db, id=record_id, schema=data)
    return {"message": "Updated record!", "record": updated_record}


@router.delete("/wordpress/{record_id}")
def deleted(
    record_id: int,
    db: Session = Depends(conn),
    token: str = Depends(token_in_header),
):
    decoded = decode_token(token)
    try:
        record = wordpress_dao.delete(db, id=record_id)

        # TODO: Turn this into middleware
        if record.blog_url != decoded["sub"]:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token",
            )
    except Exception as e:
        logger.error(e)

    return {"message": "Deleted record!"}


# Proof of concept method; talks to the Wordpress installation using provided credentials
@router.get("/wordpress/connect/{record_id}")
def retrieve_blog(
    record_id: int,
    db: Session = Depends(conn),
    token: str = Depends(token_in_header),
):
    decoded = decode_token(token)
    record = None

    try:
        record = wordpress_dao.get(db, id=record_id)
        if record is None:
            return {
                "message": f"We were unable to find a wordpress record with the id {record_id}"
            }

        # TODO: Turn this into middleware
        if record.blog_url != decoded["sub"]:
            raise HTTPException(
                status_code=401,
                detail=f"Invalid token",
            )
    except Exception as e:
        logger.error(e)
        raise e

    username = record.api_credentials["site_api_key"]
    password = record.api_credentials["site_api_password"]

    auth = HTTPBasicAuth(username, password)

    payload = {"value_one": "value1", "value_two": "value2"}

    logger.info(f"Sending a request to {record.blog_url}/{TEST_ROUTE}")

    response = requests.post(
        f"{record.blog_url}/{TEST_ROUTE}",
        auth=auth,
        json=payload,
    )

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(response.text)
        return {"message": "Request failed"}
