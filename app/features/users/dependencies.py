from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.core.db.models import User
from app.core.security import decode_access_token, get_password_hash
from app.features.users.roles import UserRoles
from app.features.users.schemas import UserCreate, UserRead


def create_user(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db.add(
        User(
            name=user_data.name,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=UserRoles.USER,
        )
    )
    db.commit()
    return UserRead(name=user_data.name, email=user_data.email)


def get_user_by_token(db: Session, token: str):
    user_id = decode_access_token(token)

    user_data = db.query(User).filter_by(id=int(user_id)).first()
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead(name=user_data.name, email=user_data.email)
