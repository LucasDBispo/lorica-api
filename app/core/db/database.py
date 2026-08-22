from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DBSettings

db_settings = DBSettings()

engine = create_engine(db_settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
