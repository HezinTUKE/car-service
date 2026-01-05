import uuid
import time
from sqlalchemy import UUID, Enum, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.enums.services.car_brands import CarBrands
from application.enums.services.car_types import CarType
from application.models.base import Base


class OfferCarCompatibilityModel(Base):
    __tablename__ = "offer_car_compatibility"

    offer_car_compatibility_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    offer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("offers.offer_id"), nullable=False, index=True)
    car_type: Mapped[CarType] = mapped_column(Enum(CarType, length=50, native_enum=False), nullable=False, index=True)
    car_brand: Mapped[CarBrands] = mapped_column(Enum(CarBrands, length=50, native_enum=False), nullable=False, index=True)
    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )

    offers: Mapped["OfferModel"] = relationship("OfferModel", back_populates="offer_car_compatibility", lazy="selectin")

    __table_args__ = (UniqueConstraint("offer_id", "car_type", "car_brand", name="uq_offer_car_type_brand"),)
