from uuid import UUID

from pydantic import Field, BaseModel, EmailStr, HttpUrl, model_validator

from application.schemas.constranits import PhoneNumber, IdentificationNumber
from application.schemas.util_schemas import AddressSchema, DescriptionSchema


class FilterServiceRequestSchema(BaseModel):
    organization_id: UUID | None = Field(default=None, description="Organization ID")
    name: str | None = Field(default=None, description="Service Name")
    city: str | None = Field(default=None, description="City")
    country: str | None = Field(default=None, description="Country")
    street: str | None = Field(default=None, description="Street Address")
    current_location: str | None = Field(default=None, description="Current location in format 'latitude,longitude'")


class AddServiceRequestSchema(BaseModel):
    name: str | None = Field(default=None)
    description: list[DescriptionSchema] = Field(..., description="Service Description")
    address: AddressSchema
    organization_id: UUID | None = Field(default=None)
    instagram: HttpUrl | None = Field(default=None, description="Instagram URL")
    twitter: HttpUrl | None = Field(default=None, description="Twitter URL")
    facebook: HttpUrl | None = Field(default=None, description="Facebook URL")
    linkedin: HttpUrl | None = Field(default=None, description="Linkedin URL")
    website: HttpUrl | None = Field(default=None, description="Website URL")
    use_organization_logo: bool = Field(default=False, description="Use organization logo")
    identification_number: IdentificationNumber
    phone_number: PhoneNumber
    email: EmailStr

    @model_validator(mode="after")
    def organization_logo_validator(self) -> "AddServiceRequestSchema":
        if self.use_organization_logo and self.organization_id is None:
            raise ValueError("organization_id is required when use_organization_logo is True")
        return self
