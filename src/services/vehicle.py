
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.core.db.models import Vehicle


def get_vehicle_quantity_by_user(user_id: int, db: Session) -> int:
    vehicle_num = db.scalar(
        select(func.count()).select_from(Vehicle).where(Vehicle.owner_id == user_id)
    )

    return vehicle_num

def create_default_vehicle_nickname(user_id: int, db: Session):
    vehicle_num = get_vehicle_quantity_by_user(user_id, db)
    if vehicle_num == 0:
        vehicle_num = ""

    return f"MyVehicle{vehicle_num}"