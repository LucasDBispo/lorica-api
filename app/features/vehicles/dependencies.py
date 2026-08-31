from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.db.models import Vehicle
from app.core.security import decode_access_token
from app.features.vehicles.schemas import VehicleCreate, VehicleRead, VehicleUpdate


def create_default_vehicle_nickname(user_id: int, db: Session):
    vehicle_num = db.scalar(
        select(func.count()).select_from(Vehicle).where(Vehicle.owner_id == user_id)
    )
    if vehicle_num == 0:
        vehicle_num = ""

    return f"MyVehicle{vehicle_num}"


def create_vehicle(vehicle_data: VehicleCreate, token: str, db: Session):
    user_id = decode_access_token(token)

    if vehicle_data.nickname is None:
        vehicle_data.nickname = create_default_vehicle_nickname(user_id, db)

    db.add(
        Vehicle(
            nickname=vehicle_data.nickname,
            license_plate=vehicle_data.license_plate,
            vehicle_type=vehicle_data.vehicle_type,
            model=vehicle_data.model,
            make=vehicle_data.make,
            year=vehicle_data.year,
            odometer=vehicle_data.odometer,
            is_active=True,
            owner_id=user_id,
        )
    )
    db.commit()

    return vehicle_data


def get_all_vehicles_by_user(token: str, db: Session):
    user_id = decode_access_token(token)

    vehicles_query = db.scalars(
        select(Vehicle).where(Vehicle.owner_id == user_id)
    ).all()

    user_vehicles = (
        VehicleRead(
            id=vehicle.id,
            nickname=vehicle.nickname,
            license_plate=vehicle.license_plate,
            vehicle_type=vehicle.vehicle_type,
            make=vehicle.make,
            model=vehicle.model,
            year=vehicle.year,
            odometer=vehicle.odometer,
            is_active=vehicle.is_active,
            owner_id=vehicle.owner_id,
        )
        for vehicle in vehicles_query
    )
    return user_vehicles


# Return the vehicle only if the user is the owner
def get_owned_vehicle(user_id: int, db: Session, vehicle_id: int) -> Vehicle | None:

    vehicle = db.scalar(
        select(Vehicle).where(Vehicle.id == vehicle_id, Vehicle.owner_id == user_id)
    )

    return vehicle


def get_user_vehicle_by_id(token: str, db: Session, vehicle_id: int) -> Vehicle:
    user_id = decode_access_token(token)

    vehicle = get_owned_vehicle(user_id, db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return vehicle


def update_vehicle_by_id(
    token: str, db: Session, vehicle_id: int, vehicle_data: VehicleUpdate
):
    user_id = decode_access_token(token)

    vehicle = get_owned_vehicle(user_id, db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for field, value in vehicle_data.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)

    db.commit()
    db.refresh(vehicle)

    vehicle_updated = VehicleRead(
        id=vehicle.id,
        nickname=vehicle.nickname,
        license_plate=vehicle.license_plate,
        vehicle_type=vehicle.vehicle_type,
        model=vehicle.model,
        make=vehicle.make,
        year=vehicle.year,
        odometer=vehicle.odometer,
        is_active=vehicle.is_active,
        owner_id=vehicle.owner_id,
    )
    return vehicle_updated


def delete_vehicle_by_id(token: str, db: Session, vehicle_id: int):
    user_id = decode_access_token(token)

    vehicle = get_owned_vehicle(user_id, db, vehicle_id)
    if vehicle is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(vehicle)
    db.commit()
