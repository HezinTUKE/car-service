import logging

from fastapi import HTTPException, status
from geopy import Location
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.models import ServiceModel, OrganizationModel
from application.schemas.service_schemas.request_schemas.service_schema import (
    FilterServiceRequestSchema,
    AddServiceRequestSchema,
)
from application.schemas.service_schemas.response_schemas.service_schema import (
    ManipulateServiceResponseSchema,
    ServiceItemSchema,
    ServiceItemsResponseSchema,
)
from application.schemas.service_schemas.response_schemas.offer_schema import OffersSchema
from application.utils.get_location import get_location


class ServiceHandler:
    logger = logging.getLogger(" ")

    @classmethod
    async def add_service(cls, service_schema: AddServiceRequestSchema, user_id: str, session: AsyncSession):
        location: Location = await get_location(
            country=service_schema.country,
            city=service_schema.city,
            street=service_schema.street,
            house_number=service_schema.house_number,
            postal_code=service_schema.postal_code,
        )

        if not location:
            return ManipulateServiceResponseSchema(status=False, msg="Address was not found")

        if service_schema.organization_id:
            org_query = select(OrganizationModel).filter(
                OrganizationModel.organization_id == service_schema.organization_id
            )
            org_query_res = await session.execute(org_query)
            org_model = org_query_res.scalar_one_or_none()

            if not org_model:
                return ManipulateServiceResponseSchema(status=False, msg="Organization doesn't exist")

        try:
            service_model = ServiceModel(
                **service_schema.model_dump(),
                owner=user_id,
                longitude=location.longitude,
                latitude=location.latitude,
                original_full_address=location.address
            )
            session.add(service_model)
            await session.commit()
            return ManipulateServiceResponseSchema(status=True, msg="Service added")
        except Exception:
            cls.logger.error("Add service error", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "service addition failed")

    @classmethod
    async def get_services(cls, service_filter: FilterServiceRequestSchema, session: AsyncSession):
        try:
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
                    ServiceItemSchema(
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
                        offers=(
                            [OffersSchema.model_validate(offer).model_dump() for offer in service.offers]
                            if service.offers
                            else []
                        ),
                    )
                    for service in services
                ],
                total=total_count,
            )
        except Exception:
            cls.logger.error("Failed to get services", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "server error")

    @classmethod
    async def get_service_by_id(cls, service_id: str, session: AsyncSession):
        try:
            service_query = (
                select(ServiceModel)
                .filter(ServiceModel.service_id == service_id)
                .options(
                    selectinload(ServiceModel.offers),
                    selectinload(ServiceModel.organization),
                )
            )

            service_query_res = await session.execute(service_query)
            service_model = service_query_res.scalar_one_or_none()
            res = ServiceItemSchema.model_validate(service_model)
            return res
        except Exception:
            cls.logger.error("Failed to get service by id", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "server error")
