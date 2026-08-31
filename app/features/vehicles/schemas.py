from typing import Annotated

from pydantic import BaseModel, BeforeValidator

from app.features.vehicles.types import VehicleType


def normalize_field(field: str | None):
    if field is None:
        return None

    return field.strip().upper()


class VehicleCreate(BaseModel):
    nickname: str | None = None
    license_plate: Annotated[str | None, BeforeValidator(normalize_field)] = None
    vehicle_type: VehicleType
    model: str | None = None
    make: str | None = None
    year: int | None = None
    odometer: int | None = None


class VehicleRead(BaseModel):
    id: int
    nickname: str
    license_plate: str | None
    vehicle_type: VehicleType
    make: str | None
    model: str | None
    year: int | None
    odometer: int | None
    is_active: bool
    owner_id: int


class VehicleUpdate(BaseModel):
    nickname: str | None = None
    license_plate: Annotated[str | None, BeforeValidator(normalize_field)] = None
    vehicle_type: VehicleType | None = None
    make: str | None = None
    model: str | None = None
    year: int | None = None
    odometer: int | None = None
    is_active: bool | None = None
