from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

from application.enums.services.car_brands import CarBrands
from application.enums.services.car_types import CarType
from application.enums.services.offer_types import OfferType


class ManipulateOfferResponseSchema(BaseModel):
    status: bool
    msg: str = Field(..., examples=["Offer added", "Service doesn't exist", "Offer updated", "Offer deleted"])


class CarCompatibilitySchema(BaseModel):
    offer_car_compatibility_id: UUID
    car_type: CarType
    car_brand: CarBrands

    model_config = ConfigDict(
        from_attributes=True,
    )


class OffersSchema(BaseModel):
    offer_id: UUID
    offer_type: OfferType
    description: str
    base_price: float
    sale: int
    currency: str
    estimated_duration_minutes: int
    offer_car_compatibility: list[CarCompatibilitySchema] = Field(default=list)

    model_config = ConfigDict(
        from_attributes=True,
    )

    @computed_field
    @property
    def current_price(self) -> float:
        if self.sale and self.sale > 0:
            discount = (self.sale / 100) * self.base_price
            return round(self.base_price - discount, 2)
        return self.base_price
