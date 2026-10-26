import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.core.db.models import Base, User
from src.core.security import create_access_token
from src.main import app
from src.repositories.user import create_user
from src.schemas.user import UserCreate
from src.tests.utils.utils import random_email, random_lower_string

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql+psycopg://postgres:postgres@test-db:5432/lorica_db_test")


@pytest.fixture(scope="session")
def test_engine() -> Generator[Engine]:
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)

    yield engine 
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def test_db(test_engine) -> Generator[Session]:
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(autouse=True)
def override_get_db(test_db: Session):
    def _override():
        yield test_db

    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client    

@pytest.fixture
def user(test_db: Session) -> User:
    user_in = UserCreate(email=random_email(), name=random_lower_string(), password="lorica12345")
    user = create_user(user_in, test_db)
    return user

@pytest.fixture
def token(user: User) -> str:
    data={"sub": str(user.id)}
    return create_access_token(data)

