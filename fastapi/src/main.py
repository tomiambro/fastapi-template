from typing import Union

import models
import schemas
from dao import wordpress_dao
from db import conn
from routes import public, utilities, wordpress
from settings import data, logger_for
from schemas import Random
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException

logger = logger_for(__name__)

app = FastAPI()
app.include_router(public.router)
app.include_router(wordpress.router)
app.include_router(utilities.router)
# app.include_router(private.router, prefix="/api/v1")


# @app.get("/")
# def read_root():
#     # logger.info("hello, world!")
#     # logger.debug("/api/log_now starts")
#     # logger.info("I'm logging")
#     # logger.warning("some warnings")
#     # logger.info(data)
#     return {"200": "OK"}


@app.get("/api/v1/")
def api_hello_v1():
    username = "9606cf61-091e-43b5-beee-e949c1895cdf"
    password = "$P$BEd/E1kWlsMBGNx3zY5Wn7lgn.5JdE1"

    auth = HTTPBasicAuth(username, password)

    payload = {"key1": "value1", "key2": "value2"}

    response = requests.post(
        "https://bullpen-wp.clone.network/wp-json/bullpenai/v1/test_route",
        auth=auth,
        json=payload,
    )

    if response.status_code == 200:
        return response.json()
    else:
        logger.error(response.text)
        return {"message": "Request failed"}
