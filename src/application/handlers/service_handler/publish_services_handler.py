import asyncio
import logging
from typing import cast

from fastapi import HTTPException, status
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from application.dataclasses.services.offer_cars_relation_dc import (
    EventData,
    ServiceDC,
    OfferCarCompatibilityModelDC,
    OfferDC,
)
from application.enums.services.country import Country
from application.enums.services.rabbit_routers import PublishRabbitRouter
from application.events.event import get_rabbit_processor
from application.models import ServiceModel


class PublishServicesHandler:
    logger = logging.getLogger(" ")

    @classmethod
    async def publish_services(cls, session: AsyncSession):
        try:
            limit, offset = 100, 0
            rabbit_mq = await get_rabbit_processor()
            row_number = await cls.count_unpublished_services(session)

            while offset <= row_number:
                data = EventData()
                services: [ServiceModel] = await cls.retrieve_unpublished_services(session, limit, offset)

                for service_model in services:
                    offers_dc: [OfferDC] = [
                        OfferDC(
                            offer_id=offer.offer_id,
                            offer_type=offer.offer_type,
                            description=offer.description,
                            currency=offer.currency,
                            base_price=offer.base_price,
                            sale=offer.sale,
                            service_id=offer.service_id,
                            estimated_duration_minutes=offer.estimated_duration_minutes,
                            created_at=offer.created_at,
                            updated_at=offer.updated_at,
                            offer_car_compatibility=[
                                OfferCarCompatibilityModelDC(**compatibility.__dict__)
                                for compatibility in offer.offer_car_compatibility
                            ],
                        )
                        for offer in service_model.offers
                    ]

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
                    data.services.append(service_dc)

                await rabbit_mq.publish(
                    routing_key=PublishRabbitRouter.PROCESS_SERVICES,
                    message=data.to_dict(),
                )

                for service in services:
                    service.is_published = True

                await session.commit()
                await asyncio.sleep(0.01)

                offset += limit

            return {"status": True}
        except Exception:
            cls.logger.error("Failed to publish services", exc_info=True)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to publish services")

    @staticmethod
    async def count_unpublished_services(session: AsyncSession) -> int:
        query = select(func.count()).select_from(ServiceModel).filter(ServiceModel.is_published == False)
        query_res = await session.execute(query)
        return query_res.scalar_one()

    @staticmethod
    async def retrieve_unpublished_services(session: AsyncSession, limit: int, offset: int) -> [ServiceModel]:
        query = select(ServiceModel).where(ServiceModel.is_published == False).limit(limit).offset(offset)
        response = await session.execute(query)
        return response.scalars().all()
