from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class CarBrandModel(Base):
    __tablename__ = 'car_brands'

    car_brand_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    car_brand_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    car_types: Mapped[list["CarTypeModel"]] = relationship("CarTypeModel", back_populates="car_brand", lazy="selectin")
