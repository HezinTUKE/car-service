import json

from moto import mock_aws
from fastapi.testclient import TestClient


@mock_aws
def test_register_success(api_client: TestClient):
    response = api_client.post(
        "/auth/signup",
        json={
            "email": "test@gmail.com",
            "password": "Test123!",
        }
    )

    assert response.status_code == 200


@mock_aws
def test_weak_password(api_client: TestClient):
    payload = {
        "email": "test@gmail.com",
        "password": "test1234",
    }

    response = api_client.post("/auth/signup", json=payload)

    assert response.status_code == 400


@mock_aws
def test_unique_email(api_client: TestClient):
    payload = {
        "email": "test@gmail.com",
        "password": "Test123!",
    }

    api_client.post("/auth/signup", json=payload)
    response = api_client.post("/auth/signup", json=payload)

    assert response.status_code == 400
