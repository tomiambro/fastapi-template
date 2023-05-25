import json

import schemas
from dao import user_dao
from db.database import Base, SessionLocal, engine
from settings.config import data
from utilities.jwt_token import get_hashed_password


class TestUserModel:
    def test_create_user(self):
        Base.metadata.create_all(bind=engine)
        try:
            db = SessionLocal()

            user_data = schemas.UserCreate(
                name="tomas",
                email="tomas@example.com",
                hashed_password=get_hashed_password("1234"),
            )
            user_dao.create(db, user_data)

            user = user_dao.get_by_field(db, "email", "tomas@example.com")
            assert user is not None
            assert user.name == "tomas"
            assert user.hashed_password != "1234"
            assert user.hashed_password == get_hashed_password("1234")

        finally:
            try:
                user_dao.delete(db, id=user.id)
            except:
                pass
