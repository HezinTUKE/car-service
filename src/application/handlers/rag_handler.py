from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from application.models import ServiceModel
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
            query = select(ServiceModel).options(
                selectinload(ServiceModel.offers)
            ).limit(limit).offset(offset)
            query_result = await session.execute(query)
            services = query_result.scalars().all()

            for service in services:
                await RagUtils.update_or_create_rag_idx(service, service.offers)

            offset += step
