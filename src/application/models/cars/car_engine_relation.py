import time

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class CarEngineRelation(Base):
    __tablename__ = "car_engine_relation"

    car_engine_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_type_id"), nullable=False, index=True)
    car_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_types.car_type_id"), nullable=False, index=True)

    created_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()), onupdate=int(time.time()))

    car_type: Mapped["CarTypeModel"] = mapped_column("CarTypeModel", primary_key=True)
    engine: Mapped["EngineModel"] = mapped_column("EngineModel", primary_key=True)
