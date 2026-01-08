from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.dataclasses.services.offer_cars_relation_dc import OfferCarRelationsListDC, OfferCarRelationDC
from application.models import ServiceModel, OfferCarCompatibilityModel, OfferModel
from application.utils.rag_utils import RagUtils


class RagHandler:
    @classmethod
    async def rag_query(cls, question: str):
        return await RagUtils.rag_query(question)

    @classmethod
    async def fill_rag_index(cls, session: AsyncSession):
        limit, offset = 100, 0
        step = 100

        count_query = select(func.count()).select_from(ServiceModel)
        total_query_res = await session.execute(count_query)
        total_count: int = total_query_res.scalar_one()

        if total_count == 0:
            return

        while offset < total_count:
            query = (
                select(ServiceModel)
                .options(
                    selectinload(ServiceModel.offers).selectinload(OfferModel.offer_car_compatibility),
                )
                .limit(limit)
                .offset(offset)
            )
            query_result = await session.execute(query)
            services = query_result.scalars().all()

            for service in services:
                offer_car_relations_dc = OfferCarRelationsListDC(
                    service_model=service,
                    offer_car_relations=[
                        OfferCarRelationDC(offer=offer, car_compatibility_models=offer.offer_car_compatibility)
                        for offer in service.offers
                    ],
                )
                await RagUtils.update_or_create_rag_idx(offer_car_relations_dc)

            offset += step
