import pytest
from starlette.testclient import TestClient
from settings.config import data
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session

from .main import app
from db import conn
from models.base_class import Base
from models import User

pytest_plugins = ("celery.contrib.pytest",)


@pytest.fixture(scope="session")
def db_engine():
    SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/test"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
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
    # db = Session(db_engine)
    app.dependency_overrides[conn] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[conn] = lambda: db

    with TestClient(app) as client:
        yield client
