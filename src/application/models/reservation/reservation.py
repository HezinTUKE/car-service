import uuid

from sqlalchemy import UUID, String, ForeignKey, Boolean, Integer, UniqueConstraint, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from application.models.base import Base


class ReservationModel(Base):
    __tablename__ = 'reservations'

    reservation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=str(uuid.uuid4()))
    schedule_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("schedule.schedule_id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    master_approved: Mapped[bool] = mapped_column(Boolean, nullable=True)
    customer_approved: Mapped[bool] = mapped_column(Boolean, nullable=True)
    urgently: Mapped[bool]= mapped_column(Boolean, nullable=True)
    car_brand: Mapped[int] = mapped_column(Integer, ForeignKey("car_brands.car_brand_id"), nullable=False)
    car_type: Mapped[int] = mapped_column(Integer, ForeignKey("car_types.car_type_id"), nullable=False)
    car_engine: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_id"), nullable=True)
    need_evacuate: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    problem_description: Mapped[str] = mapped_column(String(120), nullable=False)

    schedule: Mapped["ScheduleModel"] = relationship("ScheduleModel", back_populates="reservation", lazy="selectin")
    brand: Mapped["CarBrandModel"] = relationship("CarBrandModel", back_populates="reservation", lazy="selectin")
    type: Mapped["CarTypeModel"] = relationship("CarTypeModel", back_populates="reservation", lazy="selectin")
    engine: Mapped["EngineTypeModel"] = relationship("EngineTypeModel", back_populates="reservation", lazy="selectin")

    __mapper_args__ = UniqueConstraint('reservation_id', 'user_id', 'schedule_id')
