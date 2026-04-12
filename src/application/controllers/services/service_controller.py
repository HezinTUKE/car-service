from typing import Annotated

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import SERVICE_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.enums.roles import Roles
from application.handlers.service_handler.service_handler import ServiceHandler
from application.deps.db_deps import get_session
from application.schemas.service_schemas.request_schemas.service_schema import (
    FilterServiceRequestSchema,
    AddServiceRequestSchema,
)
from application.schemas.service_schemas.response_schemas.service_schema import (
    ManipulateServiceResponseSchema,
    ServiceItemsResponseSchema,
)


class ServiceController:
    router = APIRouter(prefix=f"/{SERVICE_CONTROLLER_PREFIX}", tags=[SERVICE_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/add-service", response_model=ManipulateServiceResponseSchema)
    async def add_service(
        current_user: Annotated[JwtDC, Depends(get_current_user)],
        request_schema: AddServiceRequestSchema = Body(...),
        session: AsyncSession = Depends(get_session),
    ):
        return await ServiceHandler.add_service(request_schema, current_user.user_id, session)

    @staticmethod
    @router.get("/get-services", response_model=ServiceItemsResponseSchema)
    async def get_services(
        service_filter: FilterServiceRequestSchema = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        return await ServiceHandler.get_services(service_filter, session)

    @staticmethod
    @router.get("/get-services-by-id")
    async def get_services_by_id(
        service_id: str,
        session: AsyncSession = Depends(get_session),
    ):
        return await ServiceHandler.get_service_by_id(service_id, session)
