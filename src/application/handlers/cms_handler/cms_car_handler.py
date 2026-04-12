from loguru import logger

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from application.enums.services.engine_type import EngineType
from application.models import CarBrandModel, CarTypeModel, EngineTypeModel
from application.models.cars.engine_type import ICEEngineModel, EVEngineModel
from application.schemas.cms.request_schemas.car_schema import (
    CreateCarTypeRequestSchema,
    CreateEVEngineRequestSchema,
    CreateICEEngineRequestSchema,
)
from application.schemas.cms.response_schemas.car_schemas import (
    ListCarResponseSchema,
    BrandItemSchema,
    ListCarTypeResponseSchema,
    CarTypeItemSchema,
    ListEnginesResponseSchema,
    ICEEngineResponseSchema,
    EVEngineResponseSchema,
)
from application.utils.exceptions import BadRequestException
from application.utils.s3_service import S3Service


class CMSCarHandler:
    engine_map = {
        EngineType.EV: EVEngineModel,
        EngineType.ICE: ICEEngineModel
    }

    def __init__(self):
        self.prefix = ["car", "brand", "logo"]

    async def add_car_brand(
        self,
        car_brand_logo: UploadFile,
        car_brand_name: str,
        session: AsyncSession,
    ):
        try:
            model = CarBrandModel(
                car_brand_name=car_brand_name,
                logo_extension=car_brand_logo.filename.split(".")[-1],
            )

            s3_service = S3Service(allowed_extensions=("svg", "png"))

            await s3_service.upload_file_to_s3(
                file=car_brand_logo,
                prefix=self.prefix,
                file_name=model.car_brand_name.upper().replace(" ", "_"),
            )

            session.add(model)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    async def get_list_brands(self, session: AsyncSession):
        try:
            stmt = select(CarBrandModel).order_by(CarBrandModel.car_brand_name.desc())
            result = await session.execute(stmt)
            records = result.scalars().all()

            s3_service = S3Service()

            return ListCarResponseSchema(
                total=len(records),
                data=[
                    BrandItemSchema(
                        brand_id=record.car_brand_id,
                        brand_name=record.car_brand_name,
                        image_url=await s3_service.generate_persist_url(
                            prefix=self.prefix,
                            file_name=f"{record.car_brand_name.upper()}.{record.logo_extension}"
                        ),
                    )
                    for record in records
                ]
            )
        except Exception:
            raise

    async def add_car_type(
        self,
        request: CreateCarTypeRequestSchema,
        session: AsyncSession
    ):
        try:
            brand = await session.get(CarBrandModel, request.brand_id)

            if not brand:
                raise BadRequestException(detail="Brand not found")

            model = CarTypeModel(
                car_type_name=request.car_type_name,
                car_brand_id=request.brand_id,
            )

            session.add(model)
            await session.commit()
        except Exception:
            await session.rollback()
            raise

    async def get_list_car_types(self, brand_name: str, session: AsyncSession):
        try:
            stmt = (select(CarBrandModel)
                    .filter(CarBrandModel.car_brand_name.ilike(brand_name))
                    .join(CarBrandModel.car_types)
                    .options(selectinload(CarBrandModel.car_types))
                    .order_by(CarTypeModel.car_type_name.desc()))

            result = await session.execute(stmt)
            record = result.scalars().first()

            if not record:
                raise BadRequestException(detail="Brand not found")

            return ListCarTypeResponseSchema(
                brand_id=record.car_brand_id,
                total=len(record.car_types),
                data=[
                    CarTypeItemSchema(
                        type_id=car_type.car_type_id,
                        type_name=car_type.car_type_name,
                    )
                    for car_type in record.car_types
                ]
            )
        except Exception:
            logger.exception("Failed to get car types", exc_info=True)
            raise

    async def add_engine(self, engine: CreateEVEngineRequestSchema | CreateICEEngineRequestSchema, session: AsyncSession):
        try:
            model_class = self.engine_map.get(engine.engine_type, None)

            if not model_class:
                raise BadRequestException(detail=f"Engine {engine.engine_type.name} not found")

            model = model_class(**engine.model_dump())
            session.add(model)
            await session.commit()
            await session.refresh(model)
        except Exception:
            await session.rollback()
            logger.exception("Failed to add engine", exc_info=True)
            raise

    async def get_list_engines(self, session: AsyncSession):
        stmt = select(EngineTypeModel).order_by(EngineTypeModel.engine_type.desc())
        result = await session.execute(stmt)
        records: [EngineTypeModel] = result.scalars().all()

        data = []

        for record in records:
            model = ICEEngineResponseSchema.model_validate(record) \
                if record.engine_type == EngineType.ICE \
                else EVEngineResponseSchema.model_validate(record)
            data.append(model)

        return ListEnginesResponseSchema(
            total=len(records),
            data=data
        )
