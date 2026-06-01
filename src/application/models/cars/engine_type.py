from sqlalchemy import Integer, String, Enum, Float, ForeignKey, Identity
from sqlalchemy.orm import Mapped, relationship, mapped_column

from application.enums.services.engine_type import EngineType
from application.models.base import Base


class EngineTypeModel(Base):
    __tablename__ = "engine_types"

    engine_id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True, autoincrement=True)
    engine_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    engine_code: Mapped[EngineType] = mapped_column(Enum(EngineType, native_enum=False, length=20), unique=True, nullable=False)

    user_car_relation: Mapped[list["UserCarRelationModel"]] = relationship("UserCarRelationModel", back_populates="engine_types")
    car_engine_relation: Mapped[list["CarEngineRelationModel"]] = relationship("CarEngineRelationModel", back_populates="engine_types", lazy="selectin")

