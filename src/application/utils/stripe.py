import os
from loguru import logger
from dotenv import load_dotenv
import stripe

from application.schemas.payment.request_schemas.price_schema import CreatePriceRequestSchema, UpdatePriceRequestSchema
from application.schemas.payment.request_schemas.product_schema import CreateProductRequestSchema
from application.utils.exceptions import ServerException

load_dotenv()


class StripeService:
    def __init__(self):
        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

    def create_product(self, product_schema: CreateProductRequestSchema):
        try:
            product = stripe.Product.create(
                name=product_schema.product_name,
                images=[product_schema.image],
            )
            return product
        except Exception:
            logger.exception("Error creating product", exc_info=True)
            raise ServerException(f"Failed to create product {product_schema.product_name}")

    def create_price(self, price_schema: CreatePriceRequestSchema, product_id: str):
        try:
            price = stripe.Price.create(
                currency=price_schema.currency.value,
                unit_amount=int(price_schema.price * 100),
                recurring=price_schema.recurring.model_dump(),
                product=product_id,
            )
            return price
        except Exception:
            logger.exception("Error creating price", exc_info=True)
            raise ServerException(f"Failed to create price for product {price_schema.product}")

    def get_product(self, product_id: str):
        try:
            product = stripe.Product.retrieve(product_id)
            return product
        except Exception:
            logger.exception("Error retrieving product", exc_info=True)
            raise ServerException(f"Failed to retrieve product with id {product_id}")

    def update_price(self, price_schema: UpdatePriceRequestSchema):
        try:
            updated_price = stripe.Price.modify(price_schema.price_id, unit_amount=int(price_schema.new_price * 100))
            return updated_price
        except Exception:
            logger.exception("Error updating price", exc_info=True)
            raise ServerException("Failed to update price")
