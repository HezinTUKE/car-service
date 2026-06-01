from __future__ import annotations
from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin
from sqlalchemy.ext.asyncio import AsyncSession

from application.deps.db_deps import get_context_session
from application.enums.services.country import Country
from application.enums.services.engine_type import EngineType
from application.models import EngineTypeModel, CarBrandModel, CarTypeModel, CarEngineRelationModel


@dataclass
class EngineTypeDTO(DataClassJsonMixin):
    id: int
    name: str
    code: EngineType


@dataclass
class CarModelDTO(DataClassJsonMixin):
    id: int
    name: str
    body_type: str
    engine_type_ids: list[int] = field(default_factory=list)


@dataclass
class CarBrandDTO(DataClassJsonMixin):
    id: int
    name: str
    country: Country
    models: list[CarModelDTO] = field(default_factory=list)


@dataclass
class JsonDTO(DataClassJsonMixin):
    engine_types: list[EngineTypeDTO] = field(default_factory=list)
    makes: list[CarBrandDTO] = field(default_factory=list)


class ImportVehicles:
    def __init__(self, json_data: dict, session: AsyncSession):
        self.session: AsyncSession = session
        self.json_data = JsonDTO.from_dict(json_data)

    @classmethod
    async def init(cls, json_data: dict):
        async with get_context_session() as session:
            inst = cls(json_data, session)
            await inst.fill_models()

    async def fill_models(self):
        try:
            await self.add_engine(self.json_data.engine_types)
            await self.add_brands(self.json_data.makes)
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise
        finally:
            await self.session.close()

    async def add_engine(self, engines: list[EngineTypeDTO]):
        engine_models = [
            EngineTypeModel(
                engine_id=engine_type.id,
                engine_name=engine_type.name,
                engine_code=engine_type.code,
            )
            for engine_type in engines
        ]

        self.session.add_all(engine_models)

    async def add_brands(self, brands: list[CarBrandDTO]):
        car_brands, car_models, engine_relations = [], [], []

        for brand in brands:
            car_models.append(CarBrandModel(
                car_brand_id=brand.id,
                car_brand_name=brand.name,
                country=brand.country,
            ))

            for model in brand.models:
                car_models.append(CarTypeModel(
                    car_type_id=model.id,
                    car_brand_id=brand.id,
                    car_type_name=model.name,
                    body_type=model.body_type,
                ))

                engine_relations.extend(CarEngineRelationModel(
                    engine_id=engine_id,
                    car_type_id=model.id,
                ) for engine_id in model.engine_type_ids)

        car_brands.extend(car_models)
        car_brands.extend(engine_relations)
        self.session.add_all(car_brands)


if __name__ == "__main__":
    import json
    import asyncio

    with open("car_seed_data.json", "r") as f:
        data = json.load(f)

    asyncio.run(ImportVehicles.init(data))
