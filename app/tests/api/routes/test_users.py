from fastapi.testclient import TestClient
from app.tests.utils.utils import random_email, random_lower_string


def test_normal_user_creation(
        client: TestClient,
):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    data = {"name": name, "email": email, "password": password}

    response = client.post("/users/", headers={"accept": "application/json"}, json=data)
    assert response.status_code == 201