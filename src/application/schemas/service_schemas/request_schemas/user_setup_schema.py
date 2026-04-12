from pydantic import BaseModel, Field


class CarRelation(BaseModel):
    car_type_id: int
    engine_id: int
    car_year: int


class CreateUserSetupSchema(BaseModel):
    name: str
    surname: str
    car_properties: list[CarRelation] = Field(default_factory=list)
