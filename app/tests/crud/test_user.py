from sqlalchemy.orm import Session

from app.features.users.dependencies import create_user
from app.features.users.roles import UserRoles
from app.features.users.schemas import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    name = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, name=name, password=password)
    user = create_user(user_in, db)
    assert user.email == email  
    assert user.name == name
    #assert user.role == UserRoles.USER
    #assert user.is_active is True
    #assert user.is_demo is False
    #assert hasattr(user, "hashed_password")
    #assert user.hashed_password != password