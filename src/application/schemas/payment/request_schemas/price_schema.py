from typing import Literal

from pydantic import BaseModel, Field, model_validator

from application.enums.services.currency import Currency


class RecurringSchema(BaseModel):
    interval: Literal["month", "day", "week", "year"] = Field(..., description="Recurring interval")
    interval_count: int = Field(default=1, description="Number of intervals between each billing cycle")

    @model_validator(mode="after")
    @classmethod
    def validate_interval_count(cls, values):
        interval = values.interval
        interval_count = values.interval_count

        if interval in ["week", "month", "year"] and 1 < interval_count:
            raise ValueError(f"For '{interval}' interval, interval_count must be 1")
        elif interval == "month" and not (1 <= interval_count <= 3):
            raise ValueError("For 'month' interval, interval_count must be between 1 and 3")

        return values


class CreatePriceRequestSchema(BaseModel):
    currency: Currency = Field(..., description="Currency")
    price: float = Field(..., description="Price")
    recurring: RecurringSchema = Field(..., description="Recurring")
    product: str = Field(..., description="Product name")


class UpdatePriceRequestSchema(BaseModel):
    price_id: str = Field(..., description="Price ID")
    new_price: float = Field(..., description="New price")
