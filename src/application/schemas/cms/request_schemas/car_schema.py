from typing import Literal

from pydantic import BaseModel, Field

from application.enums.services.engine_type import EngineType, ChargingStandard, FuelType


class CreateCarTypeRequestSchema(BaseModel):
    brand_id: int
    car_type_name: str


class CreateEngineRequestSchema(BaseModel):
    engine_name: str
    engine_type: EngineType
    power_output: float
    torque_nm: float


class CreateEVEngineRequestSchema(CreateEngineRequestSchema):
    engine_type: Literal[EngineType.EV]
    battery_capacity_kwh: float
    electric_range_km: int
    charging_standard: ChargingStandard


class CreateICEEngineRequestSchema(CreateEngineRequestSchema):
    engine_type: Literal[EngineType.ICE]
    engine_volume: float
    cylinder_count: int
    fuel_type: FuelType
