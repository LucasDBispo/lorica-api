from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import db_settings
from app.core.db.models import User
from app.core.security import get_password_hash
from app.features.users.schemas import UserCreate

engine = create_engine(db_settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db.add(
        User(
            name=user.name,
            email=user.email,
            password=get_password_hash(user.password),
            role="user",
        )
    )
    db.commit()
    return user


def get_current_user(db: Annotated[Session, Depends(get_db)]):
    db_users = db.query(User).all()
    return db_users
