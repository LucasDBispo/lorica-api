from enum import Enum


class VehicleType(str, Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    TRUCK = "truck"
    BUS = "bus"
    OTHER = "other"
