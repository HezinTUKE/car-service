from uuid import UUID

from pydantic import BaseModel

from application.enums.services.record_status import RecordStatus
from application.schemas.util_schemas import EntityItem


class AddOrganizationResponseSchema(BaseModel):
    status: bool


class OrganizationResponseSchema(BaseModel):
    organization_id: str
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
    identification_number: str
    status: RecordStatus


class OrganizationItem(EntityItem):
    organization_id: UUID


class OrganizationItemsResponseSchema(BaseModel):
    data: list[OrganizationItem]
    total: int
