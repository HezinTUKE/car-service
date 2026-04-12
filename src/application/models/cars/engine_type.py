from sqlalchemy import Integer, String, Enum, Float, ForeignKey, Identity
from sqlalchemy.orm import Mapped, relationship, mapped_column

from application.enums.services.engine_type import EngineType, ChargingStandard, FuelType
from application.models.base import Base


class EngineTypeModel(Base):
    __tablename__ = "engine_types"

    engine_id: Mapped[int] = mapped_column(Integer, Identity(always=True), primary_key=True, autoincrement=True)
    engine_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    engine_type: Mapped[EngineType] = mapped_column(Enum(EngineType, length=20, native_enum=False), nullable=False)
    power_output: Mapped[float] = mapped_column(Float, nullable=True)
    torque_nm: Mapped[float] = mapped_column(Float, nullable=True)

    # offer_car_compatibilities: Mapped[list["OfferCarCompatibilityModel"]] = relationship("OfferCarCompatibilityModel", back_populates="engine_type", lazy="selectin")
    user_car_relation: Mapped[list["UserCarRelationModel"]] = relationship("UserCarRelationModel", back_populates="engine_type", lazy="selectin")

    __mapper_args__ = {
        "polymorphic_on": engine_type,
        "polymorphic_identity": "base",
    }


class ICEEngineModel(EngineTypeModel):
    __tablename__ = "ice_engines"

    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_id"), primary_key=True)
    engine_volume: Mapped[float] = mapped_column(Float, nullable=False)
    cylinder_count: Mapped[int] = mapped_column(Integer, nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType, length=20, native_enum=False), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": EngineType.ICE.value,
        "polymorphic_load": "selectin",
    }


class EVEngineModel(EngineTypeModel):
    __tablename__ = "ev_engines"

    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_id"), primary_key=True)
    battery_capacity_kwh: Mapped[float] = mapped_column(Float, nullable=False)
    electric_range_km: Mapped[int] = mapped_column(Integer, nullable=False)
    charging_standard: Mapped[ChargingStandard] = mapped_column(Enum(ChargingStandard, length=20, native_enum=False), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": EngineType.EV.value,
        "polymorphic_load": "selectin",
    }
