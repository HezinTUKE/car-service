from typing import Annotated, Union, Literal

from pydantic import BaseModel, Field, Discriminator

from application.enums.services.engine_type import ChargingStandard, FuelType, EngineType


class BrandItemSchema(BaseModel):
    brand_id: int
    brand_name: str
    image_url: str


class ListCarResponseSchema(BaseModel):
    total: int
    data: list[BrandItemSchema] = Field(default_factory=list)


class CarTypeItemSchema(BaseModel):
    type_id: int
    type_name: str


class ListCarTypeResponseSchema(BaseModel):
    brand_id: int
    total: int
    data: list[CarTypeItemSchema] = Field(default_factory=list)


class EngineTypeItemSchema(BaseModel):
    engine_id: int
    engine_name: str
    engine_type: str


class EngineTypeResponseSchema(BaseModel):
    total: int
    data: list[EngineTypeItemSchema] = Field(default_factory=list)


class EngineResponseSchema(BaseModel):
    engine_name: str
    engine_type: EngineType
    power_output: float
    torque_nm: float

    class Config:
        from_attributes = True


class EVEngineResponseSchema(EngineResponseSchema):
    engine_type: Literal[EngineType.EV]
    battery_capacity_kwh: float
    electric_range_km: int
    charging_standard: ChargingStandard


class ICEEngineResponseSchema(EngineResponseSchema):
    engine_type: Literal[EngineType.ICE]
    engine_volume: float
    cylinder_count: int
    fuel_type: FuelType


EngineUnion = Annotated[
    Union[EVEngineResponseSchema, ICEEngineResponseSchema],
    Discriminator("engine_type")
]


class ListEnginesResponseSchema(BaseModel):
    total: int
    data: list[EngineUnion] = Field(default_factory=list)
