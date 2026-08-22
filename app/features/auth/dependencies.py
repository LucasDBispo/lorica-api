from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import create_access_token, get_password_hash, verify_password

from .schemas import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


DUMMY_HASH = get_password_hash("dummypassword")


def authenticate_user(
    db: Annotated[Session, Depends(get_db)], username: str, password: str
):
    user = db.query(User).filter_by(email=username).first()
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def login_for_token(
    db: Session,
    form_data: OAuth2PasswordRequestForm,
) -> Token:

    user_dict = authenticate_user(db, form_data.username, form_data.password)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user_dict.id)})
    return Token(access_token=access_token, token_type="bearer")
