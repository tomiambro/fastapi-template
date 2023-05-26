import pytest
from db import conn
from models import User
from models.base_class import Base
from settings.config import data
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from starlette.testclient import TestClient

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

    with TestClient(app) as client:
        yield client
