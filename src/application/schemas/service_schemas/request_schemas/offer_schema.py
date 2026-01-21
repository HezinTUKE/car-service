from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field
from application.enums.services.car_brands import CarBrands
from application.enums.services.car_types import CarType
from application.enums.services.currency import Currency
from application.enums.services.offer_types import OfferType


class CarCompatibilitySchema(BaseModel):
    car_type: CarType
    car_brand: CarBrands


class OfferSchema(BaseModel):
    offer_type: OfferType
    description: str = Field(..., min_length=10)
    currency: Currency
    base_price: Decimal = Field(..., gt=0)
    sale: int = Field(default=0, ge=0, le=100)
    estimated_duration_minutes: int = Field(..., gt=0)
    offer_car_compatibility: list[CarCompatibilitySchema] = Field(..., min_length=1, exclude=True)


class UpdateOfferSchema(OfferSchema):
    offer_id: UUID


class AddOffersRequestSchema(BaseModel):
    service_id: UUID
    offers: list[OfferSchema] = Field(..., min_length=1, max_length=50)
