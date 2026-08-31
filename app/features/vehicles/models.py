from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.features.vehicles.types import VehicleType


class VehicleModel:
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(255), nullable=False)
    license_plate: Mapped[str] = mapped_column(String(255), nullable=True)
    vehicle_type: Mapped[VehicleType] = mapped_column(
        SQLEnum(VehicleType, name="vehicle_type"), nullable=False
    )
    make: Mapped[str] = mapped_column(String(255), nullable=True)
    model: Mapped[str] = mapped_column(String(255), nullable=True)
    year: Mapped[int] = mapped_column(nullable=True)
    odometer: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
