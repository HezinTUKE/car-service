from typing import Type, Any

from sqlalchemy import select, func, Select
from sqlalchemy.ext.asyncio import AsyncSession

from application.models import ServiceModel
from application.models.services.organization import OrganizationModel


async def get_entity_result(
    base_query: Select,
    filter_dict: dict,
    model: Type[ServiceModel] | Type[OrganizationModel],
    limit: int,
    offset: int,
    session: AsyncSession,
    has_extra_fields: bool = False,
) -> tuple[int, Any]:
    count_query = select(func.count()).select_from(model).filter_by(**filter_dict)
    total_query_res = await session.execute(count_query)
    total_count: int = total_query_res.scalar_one()

    query = base_query.limit(limit).offset(offset)
    query_result = await session.execute(query)
    if not has_extra_fields:
        entities = query_result.scalars().all()
    else:
        entities = query_result.mappings().all()

    return total_count, entities
