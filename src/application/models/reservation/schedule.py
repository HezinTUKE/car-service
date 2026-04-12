import uuid
from datetime import date

from sqlalchemy import UUID, ForeignKey, Date, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class ScheduleModel(Base):
    __tablename__ = "schedule"

    schedule_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=str(uuid.uuid4()))
    service_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("services.service_id"), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, unique=True)
    start_time: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    end_time: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    day_off: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)

    reservation: Mapped[list["ReservationModel"]] = relationship("ReservationModel", back_populates="schedule", lazy="selectin")
