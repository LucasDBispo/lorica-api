from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.db.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    with Session(engine) as session:
        yield session




@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client    