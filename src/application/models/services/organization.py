import uuid
import time
from sqlalchemy import UUID, String, Text, Integer, Enum, UniqueConstraint, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.inspection import inspect
from application.enums.services.country import Country
from application.models.base import Base


class OrganizationModel(Base):
    __tablename__ = "organization"

    organization_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    country: Mapped[Country] = mapped_column(Enum(Country, native_enum=False, length=50), nullable=False, index=True)
    city: Mapped[str] = mapped_column(String, nullable=False, index=True)
    street: Mapped[str] = mapped_column(String, nullable=False, index=True)
    house_number: Mapped[str] = mapped_column(String, nullable=False, index=True)
    postal_code: Mapped[str] = mapped_column(String, nullable=False, index=True)
    phone_number: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    original_full_address: Mapped[str] = mapped_column(String, nullable=False, index=True)

    identification_number: Mapped[str] = mapped_column(String, nullable=False, index=True)
    owner: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)

    created_at = mapped_column(Integer, index=True, default=lambda: int(time.time()))
    updated_at = mapped_column(Integer, index=True, default=lambda: int(time.time()), onupdate=lambda: int(time.time()))

    services: Mapped[list["ServiceModel"]] = relationship("ServiceModel", back_populates="organization")

    __table_args__ = (
        UniqueConstraint("name", "identification_number", name="uq_service_identification_number_name"),
        UniqueConstraint("name", "owner", name="uq_owner_organization_name"),
        UniqueConstraint("name", "postal_code", name="uq_postal_code_name"),
    )

    def orm_to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
