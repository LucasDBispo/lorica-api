import random

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.db.models import User, Vehicle
from app.features.vehicles.dependencies import create_vehicle
from app.features.vehicles.schemas import VehicleCreate, VehicleRead
from app.features.vehicles.types import VehicleType
from app.tests.utils.utils import random_lower_string

def test_create_vehicle_with_all_fields(db: Session, token: str) -> None:
    nickname = random_lower_string()
    license_plate = random_lower_string()
    vehicle_type = VehicleType.TRUCK
    model = random_lower_string()
    make = random_lower_string()
    year = random.randint(1900, 2025)
    odometer = random.randint(0, 100000)

    vehicle_in = VehicleCreate(nickname=nickname, license_plate=license_plate, vehicle_type=vehicle_type, model=model, make=make, year=year, odometer=odometer)
    vehicle = create_vehicle(vehicle_in, token, db)

    assert vehicle.id is not None
    assert vehicle.nickname == nickname
    assert vehicle.license_plate == license_plate.upper()
    assert vehicle.vehicle_type == vehicle_type
    assert vehicle.model == model
    assert vehicle.make == make
    assert vehicle.year == year
    assert vehicle.odometer == odometer
    assert vehicle.is_active is True