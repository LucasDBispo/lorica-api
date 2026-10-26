from src.core.db.database import engine
from src.core.db.models import Base


def init_db():
    Base.metadata.create_all(engine)

    print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
