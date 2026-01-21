import logging

from geopy import Location
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.models.services.organization import OrganizationModel
from application.schemas.service_schemas.request_schemas.organization_schema import AddOrganizationRequestSchema
from application.schemas.util_schemas import FilterEntityRequestSchema
from application.schemas.service_schemas.response_schemas.organization_schema import \
    ManipulateOrganizationResponseSchema, OrganizationItem
from application.utils.get_location import get_location
from application.utils.handler_helpers import get_entity_result


class OrganizationHandler:
    logger = logging.getLogger(" ")

    @classmethod
    async def add_organization(cls, request_schema: AddOrganizationRequestSchema, user_id: str, session: AsyncSession):
        try:
            location: Location = await get_location(
                country=request_schema.country,
                city=request_schema.city,
                street=request_schema.street,
                house_number=request_schema.house_number,
                postal_code=request_schema.postal_code,
            )

            if not location:
                return ManipulateOrganizationResponseSchema(
                    status=False,
                    msg="Location was not found",
                )

            model = OrganizationModel(
                **request_schema.model_dump(),
                owner=user_id,
                longitude=location.longitude,
                latitude=location.latitude,
                original_full_address=location.address
            )
            session.add(model)
            return ManipulateOrganizationResponseSchema(
                status=True,
                msg="Organization was added",
            )
        except Exception:
            cls.logger.error("Failed to add organization", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def remove_organization(cls, organization_id: str, current_user: JwtDC, session: AsyncSession) -> bool:
        try:
            _query = select(OrganizationModel).filter(
                OrganizationModel.organization_id == organization_id,
            )
            _query_result = await session.execute(_query)
            organization: OrganizationModel = _query_result.scalar_one_or_none()

            if organization and organization.owner == current_user.user_id or current_user.permission == Roles.ADMIN:
                await session.delete(organization)

            return True
        except Exception:
            cls.logger.error("Failed to remove organization", exc_info=True)
            return False

    @classmethod
    async def get_organizations(
        cls, filter_model: FilterEntityRequestSchema, session: AsyncSession
    ) -> dict[str, any]:
        try:
            filter_model_dict = filter_model.model_dump(exclude_none=True)
            limit = filter_model_dict.pop("per_page", 10)
            offset = filter_model_dict.pop("page_num", 1)

            offset = offset * limit - limit
            base_query = select(OrganizationModel)

            if filter_model_dict:
                base_query = select(OrganizationModel).filter_by(**filter_model_dict)

            total_count, organizations = await get_entity_result(
                base_query=base_query,
                filter_dict=filter_model_dict,
                model=OrganizationModel,
                limit=limit,
                offset=offset,
                session=session,
            )

            return {"data": [OrganizationItem.model_validate(org) for org in organizations], "total": total_count}
        except Exception:
            cls.logger.error("Failed to get organizations", exc_info=True)
            return {"data": [], "total": 0}
