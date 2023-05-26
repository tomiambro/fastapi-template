from dao import user_dao
from utilities.jwt_token import verify_password


def test_me_endpoint(client, db):
    user = user_dao.get_by_field(db, "email", "tomas@example.com")
    assert user is not None
    assert user.name == "tomas"
    assert user.hashed_password != "1234"
    assert verify_password("1234", user.hashed_password)

    # Define the authentication credentials
    username = "tomas@example.com"
    password = "1234"

    payload = {"username": username, "password": password}

    # Send the POST request to the login endpoint
    response = client.post("users/login", data=payload)
    assert response.status_code == 200
    headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
    response = client.get("users/me", headers=headers)
    assert response.status_code == 200
