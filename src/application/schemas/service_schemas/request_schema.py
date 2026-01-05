from decimal import Decimal
from uuid import UUID

from pydantic import Field, BaseModel, EmailStr

from application.enums.services.car_brands import CarBrands
from application.enums.services.car_types import CarType
from application.enums.services.country import Country
from application.enums.services.currency import Currency
from application.enums.services.offer_types import OfferType
from application.schemas.service_schemas.schema_types import PhoneNumber, IdentificationNumber


class AddOrganizationRequestSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    country: Country = Field(default=Country.SLOVAKIA)
    city: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=2, max_length=100)
    house_number: str = Field(..., min_length=1, max_length=20)
    postal_code: str = Field(..., min_length=4, max_length=20)
    phone_number: PhoneNumber
    identification_number: IdentificationNumber
    email: EmailStr


class FilterOrganizationRequestSchema(BaseModel):
    organization_id: UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: Country | None = Field(default=None)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=4, max_length=20)
    identification_number: IdentificationNumber | None = Field(default=None)
    per_page: int = Field(default=10)
    page_num: int = Field(default=1)


class AddServiceRequestSchema(AddOrganizationRequestSchema):
    organization_id: UUID | None = Field(default=None)


class FilterServiceRequestSchema(FilterOrganizationRequestSchema):
    service_id: UUID | None = Field(default=None)


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


class AddOffersRequestSchema(BaseModel):
    service_id: UUID
    offers: list[OfferSchema] = Field(..., min_length=1, max_length=50)
