from pydantic import BaseModel, ConfigDict, Field


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
    organization_id: str


class OrganizationItemsResponseSchema(BaseModel):
    data: list[OrganizationItem]
    total: int


class ServiceItem(EntityItem):
    service_id: str
    organization_id: str | None = Field(default=None)
    organization_name: str | None = Field(default=None)


class ServiceItemsResponseSchema(BaseModel):
    data: list[ServiceItem]
    total: int
