from uuid import UUID

from pydantic import BaseModel, Field

from application.schemas.util_schemas import EntityItem


class AddOrganizationResponseSchema(BaseModel):
    status: bool


class ManipulateOrganizationResponseSchema(BaseModel):
    status: bool
    msg: str = Field(..., examples=["Organization added", "Address was not found"])


class OrganizationItem(EntityItem):
    organization_id: UUID


class OrganizationItemsResponseSchema(BaseModel):
    data: list[OrganizationItem]
    total: int
