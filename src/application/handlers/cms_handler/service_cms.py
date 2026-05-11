from fastapi import Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.models import OfferGroupModel
from application.schemas.cms.response_schemas.service_schemas import OfferGroupListSchema


class ServiceCmsHandler:
    @staticmethod
    async def create_offer(group_name: str, session: AsyncSession):
        try:
            offer_group = OfferGroupModel(name=group_name)
            session.add(offer_group)
            await session.commit()

            return Response(status_code=status.HTTP_201_CREATED)
        except Exception:
            raise


    @staticmethod
    async def get_offer_groups(session: AsyncSession):
        try:
            select_group = select(OfferGroupModel).order_by(OfferGroupModel.name.desc())
            select_group_execution = await session.execute(select_group)
            res = select_group_execution.scalars().all()
            return OfferGroupListSchema.model_validate({"data": res})
        except Exception:
            raise


    @staticmethod
    async def update_offer(session: AsyncSession, offer_group_id: int, new_group_name: str):
        try:
            offer_group = await session.get(OfferGroupModel, offer_group_id)
            offer_group.name = new_group_name
            session.add(offer_group)
            await session.commit()
            return Response(status_code=status.HTTP_200_OK)
        except Exception:
            raise
