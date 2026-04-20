from uuid import UUID

from geoalchemy2.shape import to_shape
from pydantic import BaseModel, Field, HttpUrl, EmailStr, ConfigDict, model_validator

from application.schemas.constranits import PhoneNumber, IdentificationNumber
from application.schemas.service_schemas.response_schemas.offer_schema import OffersSchema
from application.schemas.util_schemas import EntityItem, AddressSchema, DescriptionSchema


class ServiceResponseSchema(BaseModel):
    service_id: str | None = Field(None, description="Service ID")
    user_id: str | None = Field(None, description="User ID of the service owner")
    name: str | None = Field(None, description="Service name")
    logo: HttpUrl | None = Field(default=None, description="Service logo")
    photos: list[HttpUrl] | None = Field(default=None, description="Service photos")
    description: list[DescriptionSchema]
    original_full_address: str | None = Field(None, description="Service full address")
    longitude: float = Field(..., description="Service longitude")
    latitude: float = Field(..., description="Service latitude")
    organization_id: UUID | None = Field(default=None)
    instagram: HttpUrl | None = Field(default=None, description="Instagram URL")
    twitter: HttpUrl | None = Field(default=None, description="Twitter URL")
    facebook: HttpUrl | None = Field(default=None, description="Facebook URL")
    linkedin: HttpUrl | None = Field(default=None, description="Linkedin URL")
    website: HttpUrl | None = Field(default=None, description="Website URL")
    identification_number: IdentificationNumber
    phone_number: PhoneNumber
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True,
    )

    @model_validator(mode="before")
    @classmethod
    def parse_location(cls, data):
        location = None

        if hasattr(data, "location"):
            location = data.location
        elif isinstance(data, dict):
            location = data.get("location")

        if hasattr(data, "__dict__"):
            data = data.__dict__

        geo = to_shape(location)
        data["longitude"] = geo.x
        data["latitude"] = geo.y

        return data


class ServiceItemSchema(ServiceResponseSchema):
    offers: list[OffersSchema] = Field(default=list)


class ServiceListItemSchema(BaseModel):
    service_id: str = Field(..., description="Service ID")
    logo: HttpUrl = Field(..., description="Service logo")
    name: str = Field(..., description="Service name")
    distance_meters: float | None = Field(default=None, description="Service distance in meters")

    model_config = ConfigDict(from_attributes=True)

class ServiceItemsResponseSchema(BaseModel):
    data: list[ServiceListItemSchema]
    total: int
