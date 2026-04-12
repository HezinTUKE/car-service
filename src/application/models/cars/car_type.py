from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class CarTypeModel(Base):
    __tablename__ = "car_types"

    car_type_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_brand_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_brands.car_brand_id"), nullable=False, index=True)
    car_type_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    car_brand: Mapped["CarBrandModel"] = relationship("CarBrandModel", back_populates="car_types", lazy="selectin")
    # offer_car_compatibilities: Mapped[list["OfferCarCompatibilityModel"]] = relationship("OfferCarCompatibilityModel", back_populates="car_types", lazy="selectin")
    user_car_relation: Mapped[list["UserCarRelationModel"]] = relationship("UserCarRelationModel", back_populates="car_type", lazy="selectin")
    # car_engine_relation: Mapped[list["CarEngineRelationModel"]] = relationship("CarEngineRelationModel", back_populates="car_type", lazy="selectin")
