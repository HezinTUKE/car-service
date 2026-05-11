from pydantic import BaseModel, ConfigDict, Field


class OfferGroupSchema(BaseModel):
    offer_group_id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class OfferGroupListSchema(BaseModel):
    data: list[OfferGroupSchema] = Field(default_factory=list)

    model_config = ConfigDict(
        from_attributes=True,
    )
