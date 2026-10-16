import random

from sqlalchemy.orm import Session

from app.core.db.models import Vehicle
from app.features.vehicles.dependencies import (
    create_vehicle,
    get_all_vehicles_by_user,
    get_user_vehicle_by_id,
    update_vehicle_by_id,
)
from app.features.vehicles.schemas import VehicleCreate, VehicleUpdate
from app.features.vehicles.types import VehicleType
from app.tests.utils.utils import random_lower_string


def test_get_user_vehicle_by_id(token: str, test_db: Session, ) -> None:
    vehicle_in = VehicleCreate(vehicle_type=VehicleType.CAR, model = random_lower_string(), make = random_lower_string())
    vehicle = create_vehicle(vehicle_in, token, test_db)
    vehicle_get = get_user_vehicle_by_id(token, test_db, vehicle.id)
    assert vehicle_get.__dict__ == vehicle.__dict__

def test_get_all_vehicles_by_user(token: str, test_db: Session) -> None:
    vehicle_data_1 = VehicleCreate(vehicle_type=VehicleType.TRUCK, model = random_lower_string(), make = random_lower_string())
    vehicle_data_2 = VehicleCreate(vehicle_type=VehicleType.MOTORCYCLE, year = random.randint(1900, 2025), odometer = random.randint(0, 100000))

    create_vehicle(vehicle_data_1, token, test_db)
    create_vehicle(vehicle_data_2, token, test_db)

    vehicles_list = get_all_vehicles_by_user(token, test_db)
    assert len(vehicles_list) == 2


def test_create_vehicle_with_all_fields(test_db: Session, token: str) -> None:
    nickname = random_lower_string()
    license_plate = random_lower_string()
    vehicle_type = VehicleType.TRUCK
    model = random_lower_string()
    make = random_lower_string()
    year = random.randint(1900, 2025)
    odometer = random.randint(0, 100000)

    vehicle_in = VehicleCreate(nickname=nickname, license_plate=license_plate, vehicle_type=vehicle_type, model=model, make=make, year=year, odometer=odometer)
    vehicle = create_vehicle(vehicle_in, token, test_db)

    assert vehicle.id is not None
    assert vehicle.nickname == nickname
    assert vehicle.license_plate == license_plate.upper()
    assert vehicle.vehicle_type == vehicle_type
    assert vehicle.model == model
    assert vehicle.make == make
    assert vehicle.year == year
    assert vehicle.odometer == odometer
    assert vehicle.is_active is True

def test_create_vehicle_without_optional_fields(test_db: Session, token: str) -> None:
    vehicle_type = VehicleType.MOTORCYCLE
    vehicle_in = VehicleCreate(vehicle_type=vehicle_type)    
    vehicle = create_vehicle(vehicle_in, token, test_db)

    assert vehicle.id is not None
    assert vehicle.nickname is not None # nickname is generated
    assert vehicle.license_plate is None
    assert vehicle.vehicle_type == vehicle_type
    assert vehicle.model is None
    assert vehicle.make is None
    assert vehicle.year is None
    assert vehicle.odometer is None
    assert vehicle.is_active is True

def test_update_vehicle_by_id(token: str, test_db:Session) -> None:
    vehicle_in = VehicleCreate(vehicle_type=VehicleType.CAR, model = random_lower_string(), make = random_lower_string())
    vehicle = create_vehicle(vehicle_in, token, test_db)
    vehicle_data = VehicleUpdate(nickname=random_lower_string())
    updated_vehicle = update_vehicle_by_id(token, test_db, vehicle.id, vehicle_data)
    assert updated_vehicle.nickname == vehicle_data.nickname
    
