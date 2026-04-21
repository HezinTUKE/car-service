from typing import Annotated, Union

from fastapi import APIRouter, UploadFile, Form, Depends
from pydantic import Discriminator
from sqlalchemy.ext.asyncio import AsyncSession

from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.deps.db_deps import get_session
from application.handlers.cms_handler.cms_car_handler import CMSCarHandler
from application.schemas.cms.request_schemas.car_schema import (
    CreateCarTypeRequestSchema,
    CreateEVEngineRequestSchema,
    CreateICEEngineRequestSchema,
)
from application.schemas.cms.response_schemas.car_schemas import (
    ListCarResponseSchema,
    ListCarTypeResponseSchema,
    EngineTypeResponseSchema,
    ListEnginesResponseSchema,
)


class CMSCarController:
    router = APIRouter(prefix="/car")
    handler = CMSCarHandler()

    @staticmethod
    @router.post(
        path="/create-brand"
    )
    async def create_brand(
        _: Annotated[JwtDC, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
        brand_image: UploadFile,
        brand_name: str = Form(...),
    ):
        return await CMSCarController.handler.add_car_brand(
            car_brand_logo=brand_image,
            car_brand_name=brand_name,
            session=session,
        )

    @staticmethod
    @router.get(
        path="/get-list-brands",
        response_model=ListCarResponseSchema,
    )
    async def get_brands_list(
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        return await CMSCarController.handler.get_list_brands(
            session=session,
        )

    @staticmethod
    @router.post(
        path="/create-car-type"
    )
    async def create_car_type(
        _: Annotated[JwtDC, Depends(get_current_user)],
        request: CreateCarTypeRequestSchema,
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        return await CMSCarController.handler.add_car_type(
            request=request,
            session=session
        )

    @staticmethod
    @router.get(
        path="/get-list-car-types",
        response_model=ListCarTypeResponseSchema,
    )
    async def get_car_types_list(
        session: Annotated[AsyncSession, Depends(get_session)],
        brand_name: str,
    ):
        return await CMSCarController.handler.get_list_car_types(
            session=session,
            brand_name=brand_name
        )

    @staticmethod
    @router.post(
        path="/create-engine"
    )
    async def create_car_engine(
        _: Annotated[JwtDC, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
        request: Annotated[
            Union[CreateEVEngineRequestSchema, CreateICEEngineRequestSchema],
            Discriminator("engine_type")
        ],
    ):
        return await CMSCarController.handler.add_engine(
            session=session,
            engine=request,
        )

    @staticmethod
    @router.get(
        path="/get-list-engines",
        response_model=ListEnginesResponseSchema,
    )
    async def get_engines_list(
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        return await CMSCarController.handler.get_list_engines(session)
