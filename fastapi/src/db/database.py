from models.base_class import Base
from settings.config import data
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = data["postgres_url"]

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def conn():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
