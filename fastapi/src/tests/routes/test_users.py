from dao import user_dao
from utilities.jwt_token import get_hashed_password, verify_password


def test_me_endpoint(client, db, headers):
    user = user_dao.get_by_field(db, "email", "tomas@example.com")
    assert user is not None
    assert user.name == "tomas"
    assert user.hashed_password != "1234"
    assert verify_password("1234", user.hashed_password)

    response = client.get("users/me", headers=headers)
    assert response.status_code == 200


def test_signup(client):
    user_data = {
        "name": "tomas2",
        "email": "tomas2@example.com",
        "hashed_password": get_hashed_password("1234"),
    }

    response = client.post("users/signup", json=user_data)
    assert response.status_code == 200, response.json()
    # try to create a new user with the same email
    response = client.post("users/signup", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exist"


def test_incorrect_login(client):
    login_data = {"username": "juan@example.com", "password": "wrong password"}
    response = client.post("users/login", data=login_data)
    assert response.status_code == 400

    login_data = {"username": "tomas@example.com", "password": "wrong password"}
    response = client.post("users/login", data=login_data)
    assert response.status_code == 400
