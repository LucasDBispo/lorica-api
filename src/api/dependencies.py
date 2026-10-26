from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from src.core.db.database import SessionLocal
from src.core.db.models import User
from src.core.security import decode_access_token
from src.repositories.user import get_user_by_id


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(db: Annotated[Session, Depends(get_db)] , token: Annotated[str, Depends(oauth2_scheme)]) -> User:            
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise credentials_exception
    
    return user
