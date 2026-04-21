from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import OFFER_CONTROLLER_PREFIX
from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.handlers.service_handler.offers_handler import OffersHandler
from application.deps.db_deps import get_session
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
