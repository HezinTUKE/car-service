def test_get_user(api_client, user_data):
    response = api_client.get(f"https://jsonplaceholder.typicode.com/users/{user_data['id']}")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == user_data["name"]


def test_user_id(api_client, user_data):
    response = api_client.get(f"https://jsonplaceholder.typicode.com/users/{user_data['id']}")
    data = response.json()
    assert data["id"] == user_data["id"]
