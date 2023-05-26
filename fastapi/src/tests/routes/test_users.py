from dao import user_dao
from utilities.jwt_token import verify_password


def test_me_endpoint(client, db, headers):
    user = user_dao.get_by_field(db, "email", "tomas@example.com")
    assert user is not None
    assert user.name == "tomas"
    assert user.hashed_password != "1234"
    assert verify_password("1234", user.hashed_password)

    response = client.get("users/me", headers=headers)
    assert response.status_code == 200
