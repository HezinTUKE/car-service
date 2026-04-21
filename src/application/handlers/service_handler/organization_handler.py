from fastapi import UploadFile
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point
from geopy import Location
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from application.dto.jwt_dc import JwtDC
from application.enums.groups import Groups
from application.enums.services.record_status import RecordStatus
from application.models.services.organization import OrganizationModel
from application.schemas.service_schemas.request_schemas.organization_schema import AddOrganizationRequestSchema
from application.schemas.util_schemas import FilterEntityRequestSchema
from application.schemas.service_schemas.response_schemas.organization_schema import (
    OrganizationResponseSchema,
    OrganizationItem,
)
from application.utils.exceptions import ServerException, BadRequestException, NotFoundException
from application.utils.get_location import get_location
from application.utils.handler_helpers import get_entity_result
from application.utils.s3_service import S3Service


class OrganizationHandler:

    @classmethod
    async def create_organization(cls, request_schema: AddOrganizationRequestSchema, user_id: str,
                                  logo_file: UploadFile, session: AsyncSession):
        try:
            location: Location = await get_location(
                country=request_schema.country,
                city=request_schema.city,
                street=request_schema.street,
                house_number=request_schema.house_number,
                postal_code=request_schema.postal_code,
            )

            if not location:
                raise BadRequestException(detail="Location not found")

            s3_service = S3Service(allowed_extensions=("svg", "png"))
            logo_file_name = await s3_service.upload_file_to_s3(
                file=logo_file,
            )

            model = OrganizationModel(
                **request_schema.model_dump(
                    exclude={"latitude", "longitude"}
                ),
                owner=user_id,
                location=from_shape(Point(location.longitude, location.latitude), srid=4326),
                original_full_address=location.address,
            )

            session.add(model)
            await session.commit()

            await session.refresh(model)

            return cls.dump_model_to_schema(model)
        except Exception:
            await session.rollback()
            logger.exception("Failed to add organization", exc_info=True)
            raise ServerException

    @classmethod
    async def change_organization_status(cls, organization_id: str, new_status: RecordStatus, session: AsyncSession):
        try:
            record = await session.get(OrganizationModel, organization_id)

            if not record:
                raise NotFoundException("Organization not found")

            record.status = new_status

            session.add(record)
            await session.commit()
            await session.refresh(record)

            return cls.dump_model_to_schema(record)
        except Exception:
            logger.error("Failed to confirm organization", exc_info=True)
            raise ServerException

    @classmethod
    async def remove_organization(cls, organization_id: str, current_user: JwtDC, session: AsyncSession):
        try:
            _query = select(OrganizationModel).filter(
                OrganizationModel.organization_id == organization_id,
            ).with_for_update()
            _query_result = await session.execute(_query)
            organization: OrganizationModel = _query_result.scalar_one_or_none()

            if organization and organization.owner == current_user.user_id or current_user.permission == Groups.ADMIN:
                organization.status = RecordStatus.ARCHIVED

            await session.commit()
            await session.refresh(organization)

            return cls.dump_model_to_schema(organization)
        except Exception:
            logger.error("Failed to remove organization", exc_info=True)
            raise ServerException

    @classmethod
    async def get_list_organizations(cls, filter_model: FilterEntityRequestSchema, session: AsyncSession):
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
            logger.error("Failed to get organizations", exc_info=True)
            raise ServerException

    @classmethod
    async def get_organization_by_id(cls, organization_id: str, session: AsyncSession) -> OrganizationResponseSchema:
        try:
            query = select(OrganizationModel).filter(OrganizationModel.organization_id == organization_id)
            query_result = await session.execute(query)
            organization = query_result.scalar_one_or_none()

            if not organization:
                raise NotFoundException

            return cls.dump_model_to_schema(organization)
        except Exception:
            logger.error("Failed to get organization", exc_info=True)
            raise ServerException

    @staticmethod
    def dump_model_to_schema(organization: OrganizationModel) -> OrganizationResponseSchema:
        geo = to_shape(organization.location)

        return OrganizationResponseSchema(
            organization_id=organization.organization_id,
            name=organization.name,
            description=organization.description,
            country=organization.country,
            city=organization.city,
            street=organization.street,
            house_number=organization.house_number,
            postal_code=organization.postal_code,
            phone_number=organization.phone_number,
            identification_number=organization.identification_number,
            longitude=geo.x,
            latitude=geo.y,
            original_full_address=organization.original_full_address,
            status=organization.status
        )
