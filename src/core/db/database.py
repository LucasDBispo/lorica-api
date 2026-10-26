from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import DBSettings

db_settings = DBSettings()

engine = create_engine(db_settings.database_url)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

