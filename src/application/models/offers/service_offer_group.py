import uuid

from sqlalchemy import UUID, Integer, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from application.models.base import Base


"""
    ServiceOfferGroup represents a group of offers that belong to a specific service. 
    It includes details such as the offer group code and description. 
    Each service offer group is linked to a specific service through the service_id foreign key, 
    allowing for organizing offers into logical groups based on the service they belong to.
"""


class ServiceOfferGroup(Base):
    __tablename__ = "service_offer_group"

    service_offer_group_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    offer_group_code: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("services.service_id"), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False, index=True)

    services: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="service_offer_group", lazy="selectin")
    offers: Mapped[list["OfferModel"]] = relationship("OfferModel", back_populates="service_offer_group", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("service_id", "offer_group_code", name="unique_service_offer_group_code"),
    )
