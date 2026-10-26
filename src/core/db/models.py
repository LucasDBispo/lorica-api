from sqlalchemy.orm import DeclarativeBase

from src.models import UserModel, VehicleModel


class Base(DeclarativeBase):
    pass


class User(Base, UserModel):
    pass


class Vehicle(Base, VehicleModel):
    pass
