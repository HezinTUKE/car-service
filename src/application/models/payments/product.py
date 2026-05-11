import time

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from application.models.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    product_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True, unique=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[int] = mapped_column(Integer, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, default=int(time.time()), onupdate=int(time.time()))
