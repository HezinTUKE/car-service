import uuid

from sqlalchemy import UUID, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from application.models.base import Base


class PlanModel(Base):
    __tablename__ = "plan"

    plan_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)
    organization_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=True, index=True)
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=False, index=True)
    sms_number: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    email_number: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    plan_expiration: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    created_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False, default=lambda: int(uuid.uuid1().time))
    updated_at: Mapped[int] = mapped_column(Integer, index=True, nullable=False)

    service: Mapped["ServiceModel"] = relationship("ServiceModel", back_populates="plan", lazy="selectin")
    organization: Mapped["OrganizationModel"] = relationship(
        "OrganizationModel", back_populates="plan", lazy="selectin"
    )
