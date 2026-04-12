import time
import uuid

from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class UserCarRelationModel(Base):
    __tablename__ = "user_car_relation"

    user_car_relation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    car_type_id: Mapped[int] = mapped_column(Integer, ForeignKey("car_types.car_type_id"), nullable=False, index=True)
    engine_id: Mapped[int] = mapped_column(Integer, ForeignKey("engine_types.engine_id"), nullable=False, index=True)
    user_setup_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("user_setup.user_setup_id"), nullable=False, index=True)
    car_year: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()), onupdate=int(time.time()))

    user_setup = relationship("UserSetupModel", back_populates="user_car_relation", lazy="joined")
    car_type = relationship("CarTypeModel", back_populates="user_car_relation", lazy="selectin")
    engine_type = relationship("EngineTypeModel", back_populates="user_car_relation", lazy="selectin")

    __table_args__ = (
        UniqueConstraint('user_id', 'car_type_id', name="uq_user_car_relation_id"),
    )
