from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field

from application.enums.services.car_types import CarType
from application.enums.services.offer_types import OfferType


class AddOrganizationResponseSchema(BaseModel):
    status: bool


class ManipulateOrganizationResponseSchema(BaseModel):
    status: bool
    msg: str = Field(..., examples=["Organization added", "Address was not found"])


class ManipulateServiceResponseSchema(BaseModel):
    status: bool
    msg: str = Field(..., examples=["Service added", "Organization doesn't exist"])


class EntityItem(BaseModel):
    name: str
    description: str
    country: str
    city: str
    street: str
    house_number: str
    postal_code: str
    phone_number: str
    identification_number: str
    longitude: float
    latitude: float
    original_full_address: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationItem(EntityItem):
    organization_id: UUID


class OrganizationItemsResponseSchema(BaseModel):
    data: list[OrganizationItem]
    total: int


class OffersSchema(BaseModel):
    offer_id: UUID
    offer_type: OfferType
    description: str
    car_type: CarType
    base_price: float
    sale: int
    currency: str
    estimated_duration_minutes: int

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def current_price(self) -> float:
        if self.sale and self.sale > 0:
            discount = (self.sale / 100) * self.base_price
            return round(self.base_price - discount, 2)
        return self.base_price


class ServiceItem(EntityItem):
    service_id: UUID
    offers: list[OffersSchema] = Field(default=list)
    organization_id: UUID | None = Field(default=None)
    organization_name: str | None = Field(default=None)


class ServiceItemsResponseSchema(BaseModel):
    data: list[ServiceItem]
    total: int


class RagResponseItemSchema(BaseModel):
    service_id: UUID | None
    content: str
    score: float


class RagResponseSchema(BaseModel):
    data: list[RagResponseItemSchema]
