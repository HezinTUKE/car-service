from typing import Annotated

from fastapi import APIRouter, Depends, Body, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import SERVICE_CONTROLLER_PREFIX
from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.handlers.service_handler.service_handler import ServiceHandler
from application.deps.db_deps import get_session
from application.schemas.service_schemas.request_schemas.service_schema import (
    FilterServiceRequestSchema,
    AddServiceRequestSchema,
)
from application.schemas.service_schemas.response_schemas.service_schema import (
    ServiceItemsResponseSchema, ServiceResponseSchema, ServiceItemSchema,
)


class ServiceController:
    router = APIRouter(prefix=f"/{SERVICE_CONTROLLER_PREFIX}", tags=[SERVICE_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/add-service", response_model=ServiceResponseSchema)
    async def add_service(
        current_user: Annotated[JwtDC, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
        request_schema: AddServiceRequestSchema = Body(...),
    ):
        return await ServiceHandler.add_service(request_schema, current_user, session)

    @staticmethod
    @router.post("/upload-logo", response_model=ServiceResponseSchema)
    async def upload_logo(
        service_id: str,
        logo_file: UploadFile,
        session: Annotated[AsyncSession, Depends(get_session)],
        _: Annotated[JwtDC, Depends(get_current_user)],
    ):
        return await ServiceHandler.upload_logo(service_id, logo_file, session)

    @staticmethod
    @router.post("/upload-photos", response_model=ServiceResponseSchema)
    async def upload_service_photos(
        service_id: str,
        photos: list[UploadFile],
        session: Annotated[AsyncSession, Depends(get_session)],
        _: Annotated[JwtDC, Depends(get_current_user)],
    ):
        return await ServiceHandler.upload_photos(service_id, photos, session)

    @staticmethod
    @router.get("/get-services", response_model=ServiceItemsResponseSchema)
    async def get_services(
        service_filter: FilterServiceRequestSchema = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        return await ServiceHandler.get_services(service_filter, session)

    @staticmethod
    @router.put("/archive-service")
    async def archive_service(
        service_id: str,
        session: Annotated[AsyncSession, Depends(get_session)],
        current_user: Annotated[JwtDC, Depends(get_current_user)],
    ):
        return await ServiceHandler.archive_service(service_id, session, current_user.user_id)

    @staticmethod
    @router.get("/get-services-by-id", response_model=ServiceItemSchema)
    async def get_services_by_id(
        service_id: str,
        session: AsyncSession = Depends(get_session),
    ):
        return await ServiceHandler.get_service_by_id(service_id, session)
