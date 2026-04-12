import time
import uuid

from sqlalchemy import UUID, String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class UserSetupModel(Base):
    __tablename__ = "user_setup"

    user_setup_id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, nullable=False, default=int(time.time()), onupdate=int(time.time()))

    user_car_relation: Mapped[list["UserCarRelationModel"]] = relationship("UserCarRelationModel", back_populates="user_setup", lazy="joined")
