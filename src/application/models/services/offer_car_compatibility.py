import time
from sqlalchemy import UUID, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class OfferCarCompatibilityModel(Base):
    __tablename__ = "offer_car_compatibility"

    offer_car_compatibility_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    offer_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("offers.offer_id"), nullable=False, index=True
    )

    # car_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_types.car_type_id"), nullable=False, index=True)
    # engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_id"), nullable=False, index=True)

    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )

    # car_types: Mapped["CarTypeModel"] = relationship("CarTypeModel", back_populates="offer_car_compatibilities", lazy="selectin")
    # engine_type: Mapped["EngineTypeModel"] = relationship("EngineTypeModel", back_populates="offer_car_compatibilities", lazy="selectin")
    # offers: Mapped["OfferModel"] = relationship("OfferModel", back_populates="offer_car_compatibility", lazy="selectin")

    __table_args__ = (UniqueConstraint("offer_id", "car_type_id", "engine_id", name="uq_offer_car_type"),)
