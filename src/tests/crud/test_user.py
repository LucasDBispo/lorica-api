from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.core.db.models import User
from src.repositories.user import create_user
from src.schemas.user import UserCreate, UserRead, UserRoles
from src.tests.utils.utils import random_email, random_lower_string


def test_create_user(test_db: Session) -> None:
    email: str = random_email()
    name: str = random_lower_string()
    password: str = random_lower_string()
    user_in: UserCreate = UserCreate(email=email, name=name, password=password)
    user: User = create_user(user_in, test_db)
    print(user)
    assert user.email == email
    assert user.name == name
    assert user.role == UserRoles.USER
    assert user.is_active is True
    assert user.is_demo is False
    assert hasattr(user, "password_hash")
    assert user.password_hash != password

def test_read_current_user(test_db: Session, token: str) -> None:

    current_user = get_current_user(db = test_db, token = token)
    assert current_user.id is not None
    assert current_user.email is not None
    assert current_user.is_active is True
