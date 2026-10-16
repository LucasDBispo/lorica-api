from sqlalchemy.orm import Session

from app.core.db.models import User
from app.features.users.dependencies import create_user, get_user_by_token
from app.features.users.roles import UserRoles
from app.features.users.schemas import UserCreate, UserRead
from app.tests.utils.utils import random_email, random_lower_string


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

def test_get_user_by_token(test_db: Session, token: str) -> None:
    user: UserRead = get_user_by_token(test_db, token)
    assert user.id is not None
    assert user.email is not None
