from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.features.auth.dependencies import create_access_token
from app.core.db.database import engine
from app.main import app
from app.features.users.dependencies import create_user
from app.features.users.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string
from app.core.db.models import User


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    with Session(engine) as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client    


@pytest.fixture(scope="session")
def user(db: Session) -> User:
    user_in = UserCreate(email=random_email(), name=random_lower_string(), password="lorica12345")
    user = create_user(user_in, db)
    return user

@pytest.fixture(scope="session")
def token(user: User) -> str:
    data={"sub": str(user.id)}
    return create_access_token(data)