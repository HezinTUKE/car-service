import time
import uuid

from sqlalchemy import UUID, Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.enums.services.currency import Currency
from application.models.base import Base


class OfferModel(Base):
    __tablename__ = "offers"

    offer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))

    currency: Mapped[Currency] = mapped_column(Enum(Currency, length=20, native_enum=False), nullable=False, index=True)
    base_price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    sale: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    service_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False), ForeignKey("services.service_id"), nullable=False, index=True
    )
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )

    services: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="offers", lazy="selectin")
    description: Mapped[list["OfferDescriptionModel"]] = relationship("OfferDescriptionModel", back_populates="offers", lazy="selectin")

    relation_translated_offers: Mapped[list["RelationTranslatedOfferModel"]] = relationship(
        "RelationTranslatedOfferModel",
        back_populates="offer",
        lazy="selectin"
    )
