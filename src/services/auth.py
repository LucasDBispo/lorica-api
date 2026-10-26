from sqlalchemy.orm import Session

from src.core.db.models import User
from src.core.security import create_access_token, get_password_hash, verify_password
from src.repositories.user import get_user_by_email
from src.schemas.auth import Token

DUMMY_HASH = get_password_hash("dummypassword")

def authenticate_user(
    db: Session, username: str, password: str
) -> User | None: 

    user = get_user_by_email(db, email = username)
    
    if user is None:
        verify_password(password, DUMMY_HASH)
        return None
    if not verify_password(password, user.password_hash):
        return None
    
    return user


def login_for_token(
    db: Session,
    username: str,
    password: str,
) -> Token | None:

    user_dict = authenticate_user(db = db, username = username, password = password)
    if user_dict is None:
        return None 

    access_token = create_access_token(data={"sub": str(user_dict.id)})
    return Token(access_token=access_token, token_type="bearer")