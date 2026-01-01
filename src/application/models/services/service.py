import time
import uuid

from sqlalchemy import UUID, Integer, ForeignKey, String, Enum, UniqueConstraint, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.enums.services.country import Country
from application.models.base import Base


class ServiceModel(Base):
    __tablename__ = "services"

    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("organization.organization_id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    country: Mapped[Country] = mapped_column(Enum(Country, native_enum=False, length=50), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String, nullable=False, index=True)
    street: Mapped[str] = mapped_column(String, nullable=False, index=True)
    house_number: Mapped[str] = mapped_column(String, nullable=False, index=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    original_full_address: Mapped[str] = mapped_column(String, nullable=False, index=True)

    identification_number: Mapped[str] = mapped_column(String, nullable=False)
    owner: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)

    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, index=True, nullable=False, default=lambda: int(time.time()), onupdate=lambda: int(time.time())
    )

    organization: Mapped["OrganizationModel"] = relationship("OrganizationModel", back_populates="services", lazy="selectin")
    offers: Mapped[list["OfferModel"]] = relationship("OfferModel", back_populates="services")

    __table_args__ = (UniqueConstraint("name", "identification_number", name="uq_identification_number_name"),)
