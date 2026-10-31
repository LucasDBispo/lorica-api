from fastapi import status
from fastapi.testclient import TestClient

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.db.models import User
from src.core.security import create_access_token
from src.repositories.vehicle import create_vehicle
from src.schemas.user import UserCreate
from src.schemas.vehicle import VehicleCreate
from src.tests.utils.utils import random_email, random_lower_string


def test_vehicle_creation_success(client: TestClient, token: str):

    nickname = random_lower_string()
    vehicle_type = "car"

    data = {"nickname": nickname, "vehicle_type": vehicle_type}

    response = client.post(
        "/vehicles",
        headers={"Authorization": f"Bearer {token}"},
        json=data
    )

    assert response.status_code == status.HTTP_201_CREATED

def test_vehicle_creation_fail_with_missing_parameter(client: TestClient, token: str):
    nickname = random_lower_string()

    data = {"nickname": nickname}

    response = client.post(
        "vehicles",
        headers={"Authorization": f"Bearer {token}"},
        json=data
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_vehicle_creation_fail_invalid_user (client: TestClient):

   
    token = create_access_token(data={"sub": "9999999"})
    
    nickname = random_lower_string()
    vehicle_type = "car"
    data = {"nickname": nickname, "vehicle_type": vehicle_type}

    response = client.post(
        "vehicles",
        headers={"Authorization": f"Bearer {token}"},
        json=data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_all_vehicles_success(client: TestClient, user: User, test_db: Session, token: str): 

    response = client.get("/vehicles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK 

def test_get_all_vehicles_fail_with_invalid_token(client: TestClient):
    
    token = create_access_token(data={"sub": "999999999"})

    response = client.get("/vehicles", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED