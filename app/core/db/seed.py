# seed file to create the first users


from sqlalchemy.orm import Session

from app.core.config import AdminSettings
from app.core.db.database import SessionLocal
from app.core.db.models import User
from app.core.security import get_password_hash
from app.features.users.roles import UserRoles


def seed_admin(db: Session):
    admin_settings = AdminSettings()
    admin_check = db.query(User).filter_by(role=UserRoles.ADMIN).first()
    if admin_check is None:
        db.add(
            User(
                name="admin",
                email=admin_settings.admin_email,
                password_hash=get_password_hash(admin_settings.admin_password),
                role=UserRoles.ADMIN,
            )
        )


def seed_demo_user(db: Session):
    demo_check = db.query(User).filter_by(is_demo=True).first()

    if demo_check is None:
        db.add(
            User(
                name="Demo Account",
                email="demo@lorica.app",
                password_hash=get_password_hash("lorica12345"),
                role=UserRoles.USER,
                is_demo=True,
            )
        )


def seed():
    with SessionLocal() as db:
        seed_admin(db)
        seed_demo_user(db)
        db.commit()


if __name__ == "__main__":
    seed()
