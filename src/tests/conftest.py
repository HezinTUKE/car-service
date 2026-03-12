import pytest
import requests


@pytest.fixture
def api_client():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def user_data():
    return {"id": 1, "name": "Leanne Graham"}
