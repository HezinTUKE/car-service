import traceback
import uuid

from fastapi import HTTPException, status
from geopy import Location
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.models import ServiceModel, OrganizationModel, OfferModel
from application.schemas.service_schemas.request_schema import AddServiceRequestSchema, AddOffersRequestSchema
from application.schemas.service_schemas.response_schema import ManipulateServiceResponseSchema
from application.utils.get_location import get_location
from application.utils.rag_utils import RagUtils


class ServiceHandler:
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
            return ManipulateServiceResponseSchema(status=False, msg="Address was not found").model_dump()

        if service_schema.organization_id:
            org_query = select(OrganizationModel).filter(OrganizationModel.organization_id == service_schema.organization_id)
            org_query_res = await session.execute(org_query)
            org_model = org_query_res.scalar_one_or_none()

            if not org_model:
                return ManipulateServiceResponseSchema(status=False, msg="Organization doesn't exist").model_dump()

        try:
            service_model = ServiceModel(
                **service_schema.model_dump(),
                service_id=str(uuid.uuid4()),
                owner=user_id,
                longitude=location.longitude,
                latitude=location.latitude,
                original_full_address=location.address
            )
            session.add(service_model)
            return ManipulateServiceResponseSchema(status=True, msg="Service added").model_dump()
        except Exception:
            traceback.print_exc()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def add_offers(cls, offer_schema: AddOffersRequestSchema, session: AsyncSession):
        service_id = offer_schema.service_id

        service_query = select(ServiceModel).filter(ServiceModel.service_id == service_id)
        service_query_res = await session.execute(service_query)
        service_model = service_query_res.scalar_one_or_none()

        if not service_model:
            return ManipulateServiceResponseSchema(status=False, msg="Service doesn't exist").model_dump()

        try:
            offers = []
            for offer_schema in offer_schema.offers:
                offer_model = OfferModel(**offer_schema.model_dump(), service_id=str(service_id))
                session.add(offer_model)
                offers.append(offer_model)

            await RagUtils.update_or_create_rag_idx(service_model, offers)
            return ManipulateServiceResponseSchema(status=True, msg="Offer added").model_dump()
        except Exception:
            traceback.print_exc()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")
