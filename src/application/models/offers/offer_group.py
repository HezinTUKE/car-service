import time

from sqlalchemy import Integer, String, UUID, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from application.models.base import Base


"""
    OfferGroupModel represents a group of offers that can be associated with a service. 
    It includes details such as the name and group code of the offer group. 
    Each offer group can have multiple offers linked to it, 
    allowing for organizing offers into logical groups based on their characteristics or target audience.
"""


class OfferGroupModel(Base):
    __tablename__ = "offer_group"

    offer_group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    group_code: Mapped[int] = mapped_column(Integer, nullable=False, index=True, unique=True)
    create_at: Mapped[int] = mapped_column(Integer, nullable=False, index=True, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, default=int(time.time()), onupdate=int(time.time())
    )
