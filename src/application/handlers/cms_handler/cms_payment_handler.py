from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from stripe import Product
from fastapi import Response, status

from application.models.payments.product import ProductModel
from application.schemas.payment.request_schemas.price_schema import UpdatePriceRequestSchema
from application.schemas.payment.request_schemas.product_schema import CreateProductRequestSchema
from application.utils.exceptions import BadRequestException
from application.utils.stripe import StripeService


class CMSPaymentHandler:
    stripe_service = StripeService()

    @classmethod
    async def create_product(
        cls,
        product: CreateProductRequestSchema,
        session: AsyncSession,
    ):
        try:
            new_product: Product = cls.stripe_service.create_product(product)
            product_model = ProductModel(
                product_id=new_product.id,
                name=new_product.name,
                active=new_product.active,
            )
            session.add(product_model)
            await session.commit()
            return Response(status_code=status.HTTP_200_OK, content="ok")
        except Exception:
            raise

    @classmethod
    async def create_price(cls, price_schema, session: AsyncSession):
        try:
            product = select(ProductModel).filter(ProductModel.name == price_schema.product)
            product_res = await session.execute(product)
            product = product_res.scalars().first()

            if not product:
                raise BadRequestException("Product not found")

            cls.stripe_service.create_price(price_schema, product.product_id)
        except Exception:
            raise

    @classmethod
    async def update_price(cls, price_schema: UpdatePriceRequestSchema):
        try:
            cls.stripe_service.update_price(price_schema)
        except Exception:
            raise
