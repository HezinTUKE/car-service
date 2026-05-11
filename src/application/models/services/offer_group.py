import time

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


class OfferGroupModel(Base):
    __tablename__ = "offer_group"

    offer_group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)

    create_at: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=int(time.time()), onupdate=int(time.time()))

    offer: Mapped["OfferModel"] = relationship("OfferModel", back_populates="offer_group")
