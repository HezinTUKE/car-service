from typing import Annotated

from fastapi import APIRouter, Form, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.deps.auth_deps import require_groups
from application.deps.db_deps import get_session
from application.dto.jwt_dc import JwtDC
from application.enums.groups import Groups
from application.handlers.cms_handler.service_cms import ServiceCmsHandler
from application.schemas.cms.response_schemas.service_schemas import OfferGroupListSchema


class CMSServiceController:
    router = APIRouter(prefix="/services")

    @staticmethod
    @router.post(
        path="/create-offer-group",
    )
    async def create_offer(
        session: Annotated[AsyncSession, Depends(get_session)],
        _: Annotated[JwtDC, Depends(require_groups((Groups.ADMIN, Groups.MODERATOR)))],
        group_name: str = Form(max_length=25, min_length=3),
    ):
        return await ServiceCmsHandler.create_offer(group_name, session)


    @staticmethod
    @router.get(
        path="/get-offer-groups",
        response_model=OfferGroupListSchema,
    )
    async def get_offers(
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        return await ServiceCmsHandler.get_offer_groups(session)

    @staticmethod
    @router.put(
        path="/update-offer-group",
    )
    async def update_offer_group(
        _: Annotated[JwtDC, Depends(require_groups((Groups.ADMIN, Groups.MODERATOR)))],
        session: Annotated[AsyncSession, Depends(get_session)],
        offer_group_id: int,
        new_group_name: str = Form(max_length=25, min_length=3),
    ):
        return await ServiceCmsHandler.update_offer(session, offer_group_id, new_group_name)
