from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.models import User
from app.features.users.dependencies import create_user
from app.features.users.roles import UserRoles
from app.features.users.schemas import UserCreate, UserRead
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=name, password=password)
    user = create_user(user_in, db)
    assert user.email == email
    assert user.name == name
    # assert user.role == UserRoles.USER
    # assert user.is_active is True
    # assert user.is_demo is False
    # assert hasattr(user, "hashed_password")
    # assert user.hashed_password != password


def test_get_user(db: Session) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=name, password=password)
    user = create_user(user_in, db)
    stmt = select(User).where(User.email == user.email)
    user_2 = db.execute(stmt).scalar_one()
    assert user_2.email == user.email
    assert user_2.name == user.name
