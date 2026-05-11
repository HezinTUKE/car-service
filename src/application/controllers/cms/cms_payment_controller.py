from typing import Annotated

from fastapi import APIRouter, status, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.deps.db_deps import get_session
from application.handlers.cms_handler.cms_payment_handler import CMSPaymentHandler
from application.schemas.payment.request_schemas.price_schema import CreatePriceRequestSchema, UpdatePriceRequestSchema
from application.schemas.payment.request_schemas.product_schema import CreateProductRequestSchema
from application.utils.stripe import StripeService


class PaymentController:
    router = APIRouter(prefix="/payment")
    stripe_service = StripeService()

    @staticmethod
    @router.post("/create-product")
    async def create_product(
        request: CreateProductRequestSchema, session: Annotated[AsyncSession, Depends(get_session)]
    ):
        await CMSPaymentHandler.create_product(request, session)
        return Response(status_code=status.HTTP_200_OK, content="ok")

    @staticmethod
    @router.post("/create-price")
    async def create_price(request: CreatePriceRequestSchema, session: Annotated[AsyncSession, Depends(get_session)]):
        await CMSPaymentHandler.create_price(request, session)
        return Response(status_code=status.HTTP_200_OK, content="ok")

    @staticmethod
    @router.put("/update-price")
    async def update_price(request: UpdatePriceRequestSchema):
        await CMSPaymentHandler.update_price(request)
        return Response(status_code=status.HTTP_200_OK, content="ok")
