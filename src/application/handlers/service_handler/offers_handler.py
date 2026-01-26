import logging
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.dataclasses.services.offer_cars_relation_dc import (
    OfferDC,
    OfferCarCompatibilityModelDC,
    ServiceDC,
)
from application.enums.services.country import Country
from application.models import ServiceModel, OfferModel, OfferCarCompatibilityModel
from application.schemas.service_schemas.request_schemas.offer_schema import AddOffersRequestSchema, UpdateOfferSchema
from application.schemas.service_schemas.response_schemas.service_schema import ManipulateServiceResponseSchema
from application.utils.rag_utils import RagUtils


class OffersHandler:
    logger = logging.getLogger(" ")

    @classmethod
    async def add_offers(cls, offer_schema: AddOffersRequestSchema, session: AsyncSession):
        service_id = offer_schema.service_id

        service_query = select(ServiceModel).filter(ServiceModel.service_id == service_id).options()
        service_query_res = await session.execute(service_query)
        service_model = service_query_res.scalar_one_or_none()

        if not service_model:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")

        try:
            offers_dc: [OfferDC] = []
            offers_car_compatibility_dc: [OfferCarCompatibilityModelDC] = []

            for offer in offer_schema.offers:
                offer_dc = OfferDC(**offer.model_dump(), service_id=str(service_id))
                offers_dc.append(offer_dc)

                offers_car_compatibility_dc.extend(
                    [
                        OfferCarCompatibilityModelDC(**compatibility.model_dump(), offer_id=offer_dc.offer_id)
                        for compatibility in offer.offer_car_compatibility
                    ]
                )

            session.add_all([OfferModel(**dc.to_dict()) for dc in offers_dc])
            session.add_all([OfferCarCompatibilityModel(**dc.to_dict()) for dc in offers_car_compatibility_dc])

            await session.commit()
            await session.refresh(service_model, ["offers"])

            service_dc = ServiceDC(**service_model.__dict__)
            await RagUtils.update_or_create_rag_idx(service_dc)

            return ManipulateServiceResponseSchema(status=True, msg="Offer added")
        except Exception:
            cls.logger.error("Add offer error", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def update_offers(cls, update_offer_schema: UpdateOfferSchema, session: AsyncSession):
        try:
            update_query = (
                update(OfferModel)
                .filter(OfferModel.offer_id == update_offer_schema.offer_id)
                .values(**update_offer_schema.model_dump(exclude_unset=True, exclude={"offer_id"}))
                .returning(OfferModel.service_id)
            )

            update_query_res = await session.execute(update_query)
            updated_offer_service_id: str = update_query_res.scalar_one()

            service_model = await session.get(
                ServiceModel, updated_offer_service_id, options=[selectinload(ServiceModel.offers)]
            )

            offers_dc: [OfferDC] = [OfferDC(**offer.__dict__) for offer in service_model.offers]

            service_dc = ServiceDC(
                service_id=str(service_model.service_id),
                organization_id=str(service_model.organization_id) if service_model.organization_id else None,
                name=str(service_model.name),
                description=str(service_model.description),
                country=Country(service_model.country),
                city=str(service_model.city),
                street=str(service_model.street),
                house_number=str(service_model.house_number),
                postal_code=str(service_model.postal_code),
                phone_number=str(service_model.phone_number),
                email=str(service_model.email),
                longitude=cast(float, service_model.longitude),
                latitude=cast(float, service_model.latitude),
                original_full_address=str(service_model.original_full_address),
                identification_number=str(service_model.identification_number),
                owner=str(service_model.owner),
                created_at=cast(int, service_model.created_at),
                updated_at=cast(int, service_model.updated_at),
                offers=offers_dc,
            )

            await session.commit()

            await RagUtils.update_or_create_rag_idx(service_dc)
            return ManipulateServiceResponseSchema(status=True, msg="Offer updated")
        except Exception:
            cls.logger.error("Update offer error", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "server error")
