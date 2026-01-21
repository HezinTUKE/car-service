import logging
import uuid

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.dataclasses.services.offer_cars_relation_dc import OfferCarRelationsListDC, OfferCarRelationDC
from application.models import ServiceModel, OfferModel, OfferCarCompatibilityModel
from application.schemas.service_schemas.request_schemas.offer_schema import AddOffersRequestSchema, UpdateOfferSchema
from application.schemas.service_schemas.response_schemas.service_schema import ManipulateServiceResponseSchema
from application.utils.rag_utils import RagUtils


class OffersHandler:
    logger = logging.getLogger(" ")

    @classmethod
    async def add_offers(cls, offer_schema: AddOffersRequestSchema, session: AsyncSession):
        service_id = offer_schema.service_id

        service_query = select(ServiceModel).filter(ServiceModel.service_id == service_id)
        service_query_res = await session.execute(service_query)
        service_model = service_query_res.scalar_one_or_none()

        if not service_model:
            return ManipulateServiceResponseSchema(status=False, msg="Service doesn't exist")

        try:
            relations = OfferCarRelationsListDC(service_model=service_model)

            for offer in offer_schema.offers:
                offer_id = str(uuid.uuid4())
                offer_model = OfferModel(**offer.model_dump(), service_id=str(service_id), offer_id=offer_id)

                offer_car_relation = OfferCarRelationDC(offer=offer_model)

                offer_car_relation.car_compatibility_models = [
                    OfferCarCompatibilityModel(**compatibility.model_dump(), offer_id=offer_id)
                    for compatibility in offer.offer_car_compatibility
                ]

                relations.offer_car_relations.append(offer_car_relation)

            cls.logger.debug(f"add_offers relations: {relations.get_offers()}")
            cls.logger.debug(f"add_offers car_compatibility_models: {relations.get_car_compatibility_models()}")

            session.add_all(relations.get_offers())
            session.add_all(relations.get_car_compatibility_models())

            # await RagUtils.update_or_create_rag_idx(relations)
            return ManipulateServiceResponseSchema(status=True, msg="Offer added")
        except Exception:
            cls.logger.error("Add offer error", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")

    @classmethod
    async def update_offers(cls, update_offer_schema: UpdateOfferSchema, session: AsyncSession):
        try:
            query = update(OfferModel).filter(
                OfferModel.offer_id == update_offer_schema.offer_id
            ).values(
                **update_offer_schema.model_dump(exclude_unset=True, exclude={"offer_id"})
            )

            await session.execute(query)
            return ManipulateServiceResponseSchema(status=True, msg="Offer updated")
        except Exception:
            cls.logger.error("Update offer error", exc_info=True)
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "DB exception")
