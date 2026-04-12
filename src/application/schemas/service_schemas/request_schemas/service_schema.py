from uuid import UUID

from pydantic import Field, BaseModel, EmailStr, HttpUrl

from application.schemas.constranits import PhoneNumber, IdentificationNumber
from application.schemas.util_schemas import FilterEntityRequestSchema, AddressSchema, DescriptionSchema


class FilterServiceRequestSchema(FilterEntityRequestSchema):
    service_id: UUID | None = Field(default=None)


class AddServiceRequestSchema(BaseModel):
    name: str | None = Field(default=None)
    description: list[DescriptionSchema]
    address: AddressSchema
    organization_id: UUID | None = Field(default=None)
    instagram: HttpUrl | None = Field(..., description="Instagram URL")
    twitter: HttpUrl | None = Field(..., description="Twitter URL")
    facebook: HttpUrl | None = Field(..., description="Facebook URL")
    linkedin: HttpUrl | None = Field(..., description="Linkedin URL")
    website: HttpUrl | None = Field(..., description="Website URL")
    identification_number: IdentificationNumber
    phone_number: PhoneNumber
    email: EmailStr
