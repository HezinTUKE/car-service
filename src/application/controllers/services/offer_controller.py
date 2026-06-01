from typing import Annotated

from fastapi import APIRouter, Body, Depends, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import OFFER_CONTROLLER_PREFIX
from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user, require_groups
from application.enums.groups import Groups
from application.handlers.offer_handler.offer_group_handler import OfferGroupHandler
from application.handlers.service_handler.offers_handler import OffersHandler
from application.deps.db_deps import get_session
from application.schemas.cms.response_schemas.service_schemas import OfferGroupListSchema
from application.schemas.service_schemas.request_schemas.offer_schema import AddOffersRequestSchema, UpdateOfferSchema
from application.schemas.service_schemas.response_schemas.offer_schema import ManipulateOfferResponseSchema


class OfferController:
    router = APIRouter(prefix=f"/{OFFER_CONTROLLER_PREFIX}", tags=[OFFER_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/add-offers", response_model=ManipulateOfferResponseSchema)
    async def add_offers(
        request_schema: AddOffersRequestSchema = Body(...),
        _: JwtDC = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ):
        return await OffersHandler.add_offers(offer_schema=request_schema, session=session)

    @staticmethod
    @router.post("/update-offers", response_model=ManipulateOfferResponseSchema)
    async def update_offers(
        request_schema: UpdateOfferSchema = Body(...),
        _: JwtDC = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ):
        return await OffersHandler.update_offers(update_offer_schema=request_schema, session=session)

    @staticmethod
    @router.post(
        path="/create-offer-group",
    )
    async def create_offer(
        session: Annotated[AsyncSession, Depends(get_session)],
        _: Annotated[JwtDC, Depends(require_groups((Groups.SERVICE_ADMIN, Groups.SERVICE_MODERATOR)))],
        group_name: str = Form(max_length=25, min_length=3),
        service_id: str = Form(...),
        description: str = Form(max_length=50, min_length=10),
    ):
        return await OfferGroupHandler.create_offer(group_name, service_id, session)

    @staticmethod
    @router.get(
        path="/get-offer-groups",
        response_model=OfferGroupListSchema,
    )
    async def get_offers(session: Annotated[AsyncSession, Depends(get_session)], service_id: str = Query(...)):
        return await OfferGroupHandler.get_offer_groups(session)

    @staticmethod
    @router.put(
        path="/update-offer-group",
    )
    async def update_offer_group(
        _: Annotated[JwtDC, Depends(require_groups((Groups.SERVICE_ADMIN, Groups.SERVICE_MODERATOR)))],
        session: Annotated[AsyncSession, Depends(get_session)],
        offer_group_id: int,
        new_group_name: str = Form(max_length=25, min_length=3),
    ):
        return await OfferGroupHandler.update_offer(session, offer_group_id, new_group_name)
