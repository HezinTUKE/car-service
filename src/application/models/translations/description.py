from sqlalchemy import Integer, Enum, String, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from application.enums.services.language import LanguageCode
from application.models import OrganizationModel
from application.models.base import Base


class OfferDescriptionModel(Base):
    __tablename__ = "offer_description"

    description_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    offer_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("offers.offer_id"), nullable=False, index=True)
    language_code: Mapped[LanguageCode] = mapped_column(
        Enum(LanguageCode, native_enum=False, length=20), nullable=False
    )
    content: Mapped[str] = mapped_column(String(120), nullable=False)

    offers: Mapped["OfferModel"] = relationship("OfferModel", back_populates="description", lazy="selectin")


class ServiceDescriptionModel(Base):
    __tablename__ = "service_description"

    description_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("services.service_id"), primary_key=True)
    language_code: Mapped[LanguageCode] = mapped_column(
        Enum(LanguageCode, native_enum=False, length=20), nullable=False
    )
    content: Mapped[str] = mapped_column(String(120), nullable=False)

    services: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="description", lazy="selectin")


class OrganizationDescriptionModel (Base):
    __tablename__ = "organization_description"

    description_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    organization_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("organization.organization_id"), primary_key=True)
    language_code: Mapped[LanguageCode] = mapped_column(
        Enum(LanguageCode, native_enum=False, length=20), nullable=False
    )
    content: Mapped[str] = mapped_column(String(120), nullable=False)

    organization: Mapped["OrganizationModel"] = relationship("OrganizationModel", back_populates="description", lazy="selectin")
