from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.core.db.models import User, Vehicle
from src.core.security import decode_access_token
from src.schemas.vehicle import VehicleCreate, VehicleRead, VehicleUpdate
from src.services.vehicle import create_default_vehicle_nickname


def create_vehicle(vehicle_data: VehicleCreate, user: Annotated[User, Depends(get_current_user)], db: Session):

    if vehicle_data.nickname is None:
        vehicle_data.nickname = create_default_vehicle_nickname(user_id = user.id, db = db)

    vehicle =  Vehicle(
                nickname=vehicle_data.nickname,
                license_plate=vehicle_data.license_plate,
                vehicle_type=vehicle_data.vehicle_type,
                model=vehicle_data.model,
                make=vehicle_data.make,
                year=vehicle_data.year,
                odometer=vehicle_data.odometer,
                is_active=True,
                owner_id=user.id,
            )

    try: 
        db.add(
        vehicle
        )
        db.commit()
        db.refresh(vehicle)
    except IntegrityError as exc:
        db.rollback()
        if exc.orig.diag.constraint_name == "vehicles_owner_id_fkey":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user. Please try again.")

    return vehicle

def get_all_vehicles_by_user(user: Annotated[User, Depends(get_current_user)], db: Session):

    vehicles_query = db.scalars(
        select(Vehicle).where(Vehicle.owner_id == user.id)
    ).all()

    user_vehicles: list[VehicleRead] = [
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
    ]
    
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