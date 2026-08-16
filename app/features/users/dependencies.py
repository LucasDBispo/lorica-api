from typing import Annotated, Depends

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import db_settings
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
    db.add(user)
    db.commit()
    return user
