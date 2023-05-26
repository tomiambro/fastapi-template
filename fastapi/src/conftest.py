import pytest
import schemas
from dao import user_dao
from db import conn
from models import User
from models.base_class import Base
from settings.config import data
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from starlette.testclient import TestClient
from utilities import get_hashed_password

from .main import app

pytest_plugins = ("celery.contrib.pytest",)


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(data["postgres_test_url"])
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    app.dependency_overrides[conn] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[conn] = lambda: db

    user_data = schemas.UserCreate(
        name="tomas",
        email="tomas@example.com",
        hashed_password=get_hashed_password("1234"),
    )
    user_dao.create(db, user_data)

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def headers(client):
    # Define the login credentials
    username = "tomas@example.com"
    password = "1234"

    # Prepare the request payload with the login form data
    payload = {"username": username, "password": password}

    # Send the POST request to the login endpoint
    response = client.post("/users/login", data=payload)
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture(scope="function")
def user(db):
    user_data = schemas.UserCreate(
        name="tomas",
        email="tomas@example.com",
        hashed_password=get_hashed_password("1234"),
    )
    return user_dao.create(db, user_data)
