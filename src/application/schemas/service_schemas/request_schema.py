from pydantic import Field, BaseModel, EmailStr

from application.enums.services.country import Country
from application.schemas.service_schemas.schema_types import PhoneNumber, IdentificationNumber


class AddOrganizationRequestSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10, max_length=1000)
    country: Country = Field(default=Country.SLOVAKIA)
    city: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=2, max_length=100)
    house_number: str = Field(..., min_length=1, max_length=20)
    postal_code: str = Field(..., min_length=4, max_length=20)
    phone_number: PhoneNumber
    identification_number: IdentificationNumber
    email: EmailStr


class FilterOrganizationRequestSchema(BaseModel):
    organization_id: str | None = Field(default=None, min_length=1, max_length=100)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: Country | None = Field(default=None)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=4, max_length=20)
    identification_number: IdentificationNumber | None = Field(default=None)
    per_page: int = Field(default=10)
    page_num: int = Field(default=1)


class AddServiceRequestSchema(AddOrganizationRequestSchema):
    organization_id: str | None = Field(None, min_length=1, max_length=100)


class FilterServiceRequestSchema(FilterOrganizationRequestSchema):
    service_id: str | None = Field(default=None, min_length=1, max_length=100)
