from typing import Annotated

from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import decode_access_token, get_password_hash
from app.features.users.roles import UserRoles
from app.features.users.schemas import UserCreate, UserRead


def create_user(
    user_in: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    user = User(
        name=user_in.name,
        email=user_in.email,
        password_hash=get_password_hash(user_in.password),
    )
    try:
        db.add(
            user
        )

        db.commit()
        db.refresh(user)

    except IntegrityError as exc:
        db.rollback()
        if exc.orig.diag.constraint_name == "users_email_key":
            raise HTTPException(status_code=409, detail="Email already registered")

        raise

    return user

def get_user_by_token(db: Session, token: str):

    try:
        user_id = decode_access_token(token)

    except InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid Session. Please log in and try again."
        )
    user_data = db.query(User).filter_by(id=int(user_id)).first()
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead(name=user_data.name, email=user_data.email, role=user_data.role, is_demo=user_data.is_demo, is_active=user_data.is_active)