import json

import schemas
from dao import jwt_dao, wordpress_dao
from db.database import Base, SessionLocal, engine
from settings.config import data
from utilities.jwt_token import create_access_token


def test_utilities_sum(client):
    data = {"a": 1, "b": 2}
    response = client.post("api/v1/utilities/sum", params=data)
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "The sum task has been scheduled"}


def test_public_token(client):
    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        hash_value = data["hash_value"]

        blog_data = schemas.WordpressCreate(
            blog_url="https://wordpress.org/",
            blog_name="Test Wordpress",
            blog_description="This is a test blog",
            wordpress_db_version="1",
            wordpress_site_version="1",
            wordpress_user_email="test@test.com",
        )

        blog = wordpress_dao.create(db, obj_in=blog_data)
        response = client.post(f"api/v1/public/token/{hash_value}")

        assert response.status_code == 200
        response_data = json.loads(response.content)
        tokens = jwt_dao.get_all(db)
        assert len(tokens) == 1
        token = tokens[0]
        assert token.wordpress == blog
        assert blog.token.id == token.id
        assert "access_token" in response_data
    finally:
        try:
            jwt_dao.delete(db, id=token.id)
        except:
            pass
        try:
            wordpress_dao.delete(db, id=blog.id)
        except:
            pass

        db.close()
        Base.metadata.drop_all(bind=engine)


def test_get_current_token(client):
    token = create_access_token("https://wordpress.org/")
    route = f"api/v1/public/current_token"
    response = client.get(route, params={"token": token})
    assert response.status_code == 200, response.json()


def test_get_wordpress_blog(client):
    token = create_access_token("https://wordpress.org/")
    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()

        blog_data = schemas.WordpressCreate(
            blog_url="https://wordpress.org/",
            blog_name="Test Wordpress",
            blog_description="This is a test blog",
            wordpress_db_version="1",
            wordpress_site_version="1",
            wordpress_user_email="test@test.com",
        )

        blog = wordpress_dao.create(db, obj_in=blog_data)
        route = f"api/v1/wordpress/{blog.id}"
        response = client.get(route, params={"token": token})
        assert response.status_code == 200, response.json()
    finally:
        try:
            wordpress_dao.delete(db, id=blog.id)
        except:
            pass
