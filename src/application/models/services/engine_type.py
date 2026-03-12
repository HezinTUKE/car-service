from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from application.models.base import Base


class EngineTypeModel(Base):
    __tablename__ = "engine_types"

    engine_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    engine_type_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    offer_car_compatibilities: Mapped[list["OfferCarCompatibilityModel"]] = relationship("OfferCarCompatibilityModel", back_populates="engine_type", lazy="selectin")
