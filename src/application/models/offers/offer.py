import time
import uuid

from sqlalchemy import UUID, Enum, Float, ForeignKey, Text, Integer, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.enums.services.currency import Currency
from application.models.base import Base


"""
    OfferModel represents a specific offer for a service, including details such as price, description, and compatibility. 
    It is linked to an OfferGroupModel, which can group multiple offers together. 
    Each offer is associated with a specific service and can have multiple compatibilities defined in the OfferCarCompatibilityModel.
"""


class OfferModel(Base):
    __tablename__ = "offers"

    offer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))

    currency: Mapped[Currency] = mapped_column(Enum(Currency, length=20, native_enum=False), nullable=False, index=True)
    service_offer_group_id: Mapped[int] = mapped_column(
        UUID(as_uuid=False), ForeignKey("service_offer_group.service_offer_group_id"), nullable=False, index=True
    )
    base_price: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    sale: Mapped[int] = mapped_column(Integer, nullable=True, index=True)

    description: Mapped[str] = mapped_column(String, nullable=False, index=True)
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )

    service_offer_group: Mapped["ServiceOfferGroup"] = relationship("ServiceOfferGroup", back_populates="offers", lazy="selectin")
