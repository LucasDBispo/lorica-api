from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db.database import get_db
from app.features.auth.dependencies import oauth2_scheme
from app.features.vehicles.dependencies import (
    create_vehicle,
    delete_vehicle_by_id,
    get_all_vehicles_by_user,
    get_user_vehicle_by_id,
    update_vehicle_by_id,
)
from app.features.vehicles.schemas import VehicleCreate, VehicleUpdate

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def register_vehicle(
    vehicle_data: VehicleCreate,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    return create_vehicle(vehicle_data, token, db)


@router.get("/{vehicle_id}")
def get_vehicle(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    vehicle_id: int,
):
    return get_user_vehicle_by_id(token, db, vehicle_id)


@router.get("/")
def get_all_user_vehicles(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
):
    return get_all_vehicles_by_user(token, db)


@router.patch("/{vehicle_id}")
def update_vehicle(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
):
    return update_vehicle_by_id(token, db, vehicle_id, vehicle_data)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)],
    vehicle_id: int,
):
    return delete_vehicle_by_id(token, db, vehicle_id)
