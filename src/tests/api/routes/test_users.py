from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.core.security import create_access_token
from src.repositories.user import create_user
from src.schemas.user import UserCreate
from src.services.auth import login_for_token
from src.tests.utils.utils import random_email, random_lower_string


def test_user_creation_success(
        client: TestClient,
):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    data = {"name": name, "email": email, "password": password}

    response = client.post("/users/", headers={"accept": "application/json"}, json=data)
    assert response.status_code == status.HTTP_201_CREATED

def test_user_creation_fail_with_missing_data(
        client: TestClient
):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

    data_1 = {"name": name, "password": password}
    response_1 = client.post("/users/", headers={"accept": "application/json"}, json=data_1)

    data_2 = {"name": name, "email": email}
    response_2 = client.post("/users/", headers={"accept": "application/json"}, json= data_2)

    data_3 = {"email": email, "password": password}
    response_3 = client.post("/users/", headers={"accept": "application/json"}, json=data_3)


    assert response_1.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response_2.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT      
    assert response_3.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_user_fail_with_duplicated_email( client: TestClient, test_db: Session):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()

    user_in = UserCreate(name = name, email = email, password = password)
    create_user(user_in = user_in, db = test_db)

    new_name = random_lower_string()
    new_password = random_lower_string()
    data = {"name": new_name, "email": email, "password": new_password}

    response = client.post("/users/", json=data)
    assert response.status_code == status.HTTP_409_CONFLICT
    

def test_read_user_me_success(
        client: TestClient,
        test_db: Session,
):
    name = random_lower_string()
    email = random_email()
    password = random_lower_string()
    user = create_user(user_in = UserCreate(name=name, email=email, password=password), db = test_db)
    token = login_for_token(db = test_db, username = user.email, password = password)    
    
    response = client.get("/users/me", headers={"accept": "application/json", "Authorization": f"Bearer {token.access_token}"})
    
    assert response.status_code == status.HTTP_200_OK

def test_read_user_me_fail_with_fake_user(client: TestClient, test_db: Session):
    
    access_token = create_access_token(data = {"sub": "999999999"})

    response = client.get("/users/me", headers={"accept": "application/json", "Authorization": f"Bearer {access_token}"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_read_user_me_fail_with_fake_token(client: TestClient, test_db: Session):
    fake_token = random_lower_string()

    response = client.get("/users/me", headers={"accept": "application/json", "Authorization": f"Bearer {fake_token}"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

