from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.db.models import User
from src.core.security import get_password_hash
from src.schemas.user import UserCreate


def create_user(
    user_in: UserCreate,
    db: Session,
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

def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    user = db.scalar(stmt)

    return user

def get_user_by_email(db: Session, email: str) -> User | None:  
    stmt = select(User).where(User.email == email)
    user = db.scalar(stmt)

    return user