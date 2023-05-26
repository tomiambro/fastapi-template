from utilities.jwt_token import create_access_token


def test_utilities_sum(client):
    data = {"a": 1, "b": 2}
    response = client.post("api/v1/utilities/sum", params=data)
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "The sum task has been scheduled"}


def test_get_current_token(client):
    token = create_access_token("https://wordpress.org/")
    route = f"api/v1/public/current_token"
    response = client.get(route, params={"token": token})
    assert response.status_code == 200, response.json()
