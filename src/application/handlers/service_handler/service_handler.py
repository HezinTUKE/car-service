from fastapi import UploadFile, Response
from loguru import logger
from geopy import Location
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from shapely.geometry import Point
from geoalchemy2.shape import from_shape, to_shape
from application.models import ServiceModel, OrganizationModel, ServiceDescriptionModel
from application.schemas.service_schemas.request_schemas.service_schema import (
    FilterServiceRequestSchema,
    AddServiceRequestSchema,
)
from application.schemas.service_schemas.response_schemas.service_schema import (
    ServiceItemSchema,
    ServiceItemsResponseSchema, ServiceResponseSchema,
)
from application.schemas.service_schemas.response_schemas.offer_schema import OffersSchema
from application.utils.exceptions import DBException, BadRequestException, ServerException
from application.utils.get_location import get_location
from application.utils.handler_helpers import get_entity_result
from application.utils.s3_service import S3Service


class ServiceHandler:

    @classmethod
    async def add_service(cls, service_schema: AddServiceRequestSchema, user_id: str, session: AsyncSession):
        location: Location = await get_location(
            country=service_schema.address.country,
            city=service_schema.address.city,
            street=service_schema.address.street,
            house_number=service_schema.address.house_number,
            postal_code=service_schema.address.postal_code,
        )

        if not location:
            raise BadRequestException("Location not found")

        if service_schema.organization_id:
            org_query = select(OrganizationModel).filter(
                OrganizationModel.organization_id == service_schema.organization_id
            )
            org_query_res = await session.execute(org_query)
            org_model = org_query_res.scalar_one_or_none()

            if not org_model:
                raise BadRequestException("organization not found")

        try:
            service_model = ServiceModel(
                name=service_schema.name,
                organization_id=service_schema.organization_id,
                country=service_schema.address.country,
                city=service_schema.address.city,
                street=service_schema.address.street,
                house_number=service_schema.address.house_number,
                postal_code=service_schema.address.postal_code,
                phone_number=service_schema.phone_number,
                email=service_schema.email,
                user_id=user_id,
                location=from_shape(Point(location.longitude, location.latitude), srid=4326),
                original_full_address=location.address,
                is_published=False,
                instagram=service_schema.instagram.encoded_string() or None,
                facebook=service_schema.facebook.encoded_string() or None,
                twitter=service_schema.twitter.encoded_string() or None,
                website=service_schema.website.encoded_string() or None,
                identification_number=service_schema.identification_number,
            )
            session.add(service_model)
            await session.flush()

            descriptions = [
                ServiceDescriptionModel(
                    service_id=service_model.service_id,
                    content=description.content,
                    language_code=description.language_code,
                ) for description in service_schema.description
            ]

            session.add_all(descriptions)
            await session.commit()

            return ServiceResponseSchema(
                service_id=service_model.service_id,
                name=service_model.name,
                description=service_schema.description,
                phone_number=service_model.phone_number,
                identification_number=service_model.identification_number,
                email=service_model.email,
                longitude=location.longitude,
                latitude=location.latitude,
                original_full_address=location.address,
                organization_id=service_model.organization_id,
                user_id=service_model.user_id,
            )

        except Exception:
            await session.rollback()
            logger.exception("Add service error", exc_info=True)
            raise

    @classmethod
    async def upload_logo(cls, service_id: str, logo: UploadFile, session: AsyncSession):
        try:
            service = await session.get(ServiceModel, service_id)
            if not service:
                raise BadRequestException("Service not found")

            s3 = S3Service(allowed_extensions=("jpg", "jpeg", "png", "webp"))
            await s3.upload_file_to_s3(
                file_name=service_id,
                file=logo,
                prefix=["services", "logo"],
            )
            return Response(status_code=200, content="ok")
        except Exception:
            logger.exception("Add logo error", exc_info=True)
            raise

    @classmethod
    async def upload_photos(cls, service_id: str, photos: list[UploadFile], session: AsyncSession):
        try:
            if len(photos) > 5:
                raise BadRequestException("You can upload up to 5 photos")

            service = await session.get(ServiceModel, service_id)
            if not service:
                raise BadRequestException("Service not found")

            s3 = S3Service(allowed_extensions=("jpg", "jpeg", "png", "webp"))
            for photo in photos:
                await s3.upload_file_to_s3(
                    file_name=photo.filename.split(".")[0],
                    file=photo,
                    prefix=["services", "photos", service_id],
                )

            return Response(status_code=200, content="ok")
        except Exception:
            logger.exception("Add photos error", exc_info=True)
            raise

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

            total_count, services = await get_entity_result(
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
            logger.exception("Failed to get services", exc_info=True)
            raise DBException()

    @classmethod
    async def get_service_by_id(cls, service_id: str, session: AsyncSession):
        try:
            service_query = (
                select(ServiceModel)
                .filter(ServiceModel.service_id == service_id)
                .options(
                    selectinload(ServiceModel.offers),
                    selectinload(ServiceModel.description),
                )
            )

            service_query_res = await session.execute(service_query)
            service = service_query_res.scalar_one_or_none()
            return ServiceItemSchema.model_validate(service)
        except Exception:
            logger.exception("Failed to get service by id", exc_info=True)
            raise ServerException()
