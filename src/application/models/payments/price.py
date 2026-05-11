import time

from sqlalchemy import Integer, ForeignKey, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from application.enums.services.country import Country
from application.enums.services.currency import Currency
from application.models import Base


class PriceModel(Base):
    __tablename__ = "prices"

    price_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=True)
    price: Mapped[float] = mapped_column(Integer, nullable=False)
    country: Mapped[Country] = mapped_column(Enum(Country, native_enum=False, length=50), nullable=False)
    currency: Mapped[Currency] = mapped_column(Enum(Currency, native_enum=False, length=10), nullable=False)
    created_at: Mapped[int] = mapped_column(Integer, default=int(time.time()))
    updated_at: Mapped[int] = mapped_column(Integer, default=int(time.time()), onupdate=int(time.time()))
