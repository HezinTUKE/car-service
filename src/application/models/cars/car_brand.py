from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.enums.services.country import Country
from application.models.base import Base


class CarBrandModel(Base):
    __tablename__ = "car_brands"

    car_brand_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_brand_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    country: Mapped[Country] = mapped_column(Enum(Country, native_enum=False, length=20), index=True, unique=False)

    car_model: Mapped[list["CarTypeModel"]] = relationship("CarTypeModel", back_populates="car_brand")
    car_types: Mapped[list["CarTypeModel"]] = relationship("CarTypeModel", back_populates="car_brand", lazy="selectin")
