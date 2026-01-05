import traceback
from typing import Type

from geopy import Location
from fastapi import HTTPException, status
from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.models import ServiceModel, OfferModel
from application.models.services.organization import OrganizationModel
from application.schemas.service_schemas.request_schema import (
    AddOrganizationRequestSchema,
    FilterOrganizationRequestSchema,
    FilterServiceRequestSchema,
)
from application.schemas.service_schemas.response_schema import (
    OrganizationItem,
    ServiceItem,
    ServiceItemsResponseSchema,
    ManipulateOrganizationResponseSchema,
    OffersSchema,
)
from application.utils.get_location import get_location


class OrganizationHandler:
    @classmethod
    async def add_organization(cls, request_schema: AddOrganizationRequestSchema, user_id: str, session: AsyncSession) -> dict:
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
                ).model_dump()

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
            ).model_dump()
        except Exception:
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
            return False

    @classmethod
    async def _get_entity_result(
        cls,
        base_query: Select,
        filter_dict: dict,
        model: Type[ServiceModel] | Type[OrganizationModel],
        limit: int,
        offset: int,
        session: AsyncSession,
    ) -> tuple[int, any]:
        count_query = select(func.count()).select_from(model).filter_by(**filter_dict)
        total_query_res = await session.execute(count_query)
        total_count: int = total_query_res.scalar_one()

        query = base_query.limit(limit).offset(offset)
        query_result = await session.execute(query)
        entities = query_result.scalars().all()

        return total_count, entities

    @classmethod
    async def get_organizations(cls, filter_model: FilterOrganizationRequestSchema, session: AsyncSession) -> dict[str, any]:
        try:
            filter_model_dict = filter_model.model_dump(exclude_none=True)
            limit = filter_model_dict.pop("per_page", 10)
            offset = filter_model_dict.pop("page_num", 1)

            offset = offset * limit - limit
            base_query = select(OrganizationModel)

            if filter_model_dict:
                base_query = select(OrganizationModel).filter_by(**filter_model_dict)

            total_count, organizations = await cls._get_entity_result(
                base_query=base_query, filter_dict=filter_model_dict, model=OrganizationModel, limit=limit, offset=offset, session=session
            )

            return {"data": [OrganizationItem.model_validate(org).model_dump() for org in organizations], "total": total_count}
        except Exception:
            traceback.print_exc()
            return {"data": [], "total": 0}

    @classmethod
    async def get_services(cls, service_filter: FilterServiceRequestSchema, session: AsyncSession):
        service_filter_dict = service_filter.model_dump(exclude_none=True)
        limit = service_filter_dict.pop("per_page", 10)
        offset = service_filter_dict.pop("page_num", 1)

        offset = offset * limit - limit
        base_query = select(ServiceModel)

        if service_filter_dict:
            base_query = base_query.filter_by(**service_filter_dict)

        base_query = base_query.options(
            selectinload(ServiceModel.organization),
            selectinload(ServiceModel.offers),
        )

        total_count, services = await cls._get_entity_result(
            base_query=base_query,
            filter_dict=service_filter_dict,
            model=ServiceModel,
            limit=limit,
            offset=offset,
            session=session,
        )

        return ServiceItemsResponseSchema(
            data=[
                ServiceItem(
                    service_id=service.service_id,
                    name=service.name,
                    description=service.description,
                    country=service.country,
                    city=service.city,
                    street=service.street,
                    house_number=service.house_number,
                    postal_code=service.postal_code,
                    phone_number=service.phone_number,
                    identification_number=service.identification_number,
                    email=service.email,
                    longitude=service.longitude,
                    latitude=service.latitude,
                    original_full_address=service.original_full_address,
                    organization_id=service.organization_id,
                    organization_name=service.organization.name if service.organization else None,
                    offers=[OffersSchema.model_validate(offer).model_dump() for offer in service.offers] if service.offers else [],
                )
                for service in services
            ],
            total=total_count,
        ).model_dump()
