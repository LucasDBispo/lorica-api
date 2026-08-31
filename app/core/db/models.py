from sqlalchemy.orm import DeclarativeBase

from app.features.users.models import UserModel
from app.features.vehicles.models import VehicleModel


class Base(DeclarativeBase):
    pass


class User(Base, UserModel):
    pass


class Vehicle(Base, VehicleModel):
    pass
