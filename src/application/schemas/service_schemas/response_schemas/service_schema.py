from uuid import UUID

from pydantic import BaseModel, Field

from application.schemas.service_schemas.response_schemas.offer_schema import OffersSchema
from application.schemas.util_schemas import EntityItem


class ManipulateServiceResponseSchema(BaseModel):
    status: bool
    msg: str = Field(..., examples=["Service added", "Organization doesn't exist"])


class ServiceItemSchema(EntityItem):
    service_id: UUID
    organization_id: UUID | None = Field(default=None)
    organization_name: str | None = Field(default=None)
    offers: list[OffersSchema] = Field(default=list)


class ServiceItemsResponseSchema(BaseModel):
    data: list[ServiceItemSchema]
    total: int
