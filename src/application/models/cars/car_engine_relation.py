from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class CarEngineRelationModel(Base):
    __tablename__ = "car_engine_relation"

    car_engine_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    engine_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("engine_types.engine_id"), nullable=False, index=True
    )
    car_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_model.car_type_id"), nullable=False, index=True)

    car_type: Mapped["CarTypeModel"] = relationship("CarTypeModel", back_populates="car_engine_relation", lazy="selectin")
    engine_types: Mapped["EngineTypeModel"] = relationship("EngineTypeModel", back_populates="car_engine_relation", lazy="selectin")
