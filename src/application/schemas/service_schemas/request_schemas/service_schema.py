from uuid import UUID

from pydantic import Field

from application.schemas.service_schemas.request_schemas.organization_schema import AddOrganizationRequestSchema
from application.schemas.util_schemas import FilterEntityRequestSchema


class FilterServiceRequestSchema(FilterEntityRequestSchema):
    service_id: UUID | None = Field(default=None)


class AddServiceRequestSchema(AddOrganizationRequestSchema):
    organization_id: UUID | None = Field(default=None)
