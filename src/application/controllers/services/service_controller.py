from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import SERVICE_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.handlers.service_handler.service_handler import ServiceHandler
from application.deps.db_deps import DBModel
from application.schemas.service_schemas.request_schemas.service_schema import (
    FilterServiceRequestSchema,
    AddServiceRequestSchema,
)
from application.schemas.service_schemas.response_schemas.service_schema import (
    ManipulateServiceResponseSchema,
    ServiceItemsResponseSchema,
)
from application.utils.password_utils import permission_required


class ServiceController:
    router = APIRouter(prefix=f"/{SERVICE_CONTROLLER_PREFIX}", tags=[SERVICE_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/add-service", response_model=ManipulateServiceResponseSchema)
    async def add_service(
        request_schema: AddServiceRequestSchema = Body(...),
        current_user: JwtDC = Depends(permission_required((Roles.MASTER, Roles.USER))),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await ServiceHandler.add_service(request_schema, current_user.user_id, session)

    @staticmethod
    @router.get("/get-services", response_model=ServiceItemsResponseSchema)
    async def get_services(
        service_filter: FilterServiceRequestSchema = Depends(),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await ServiceHandler.get_services(service_filter, session)

    @staticmethod
    @router.get("/get-services-by-id")
    async def get_services_by_id(
        service_id: str,
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await ServiceHandler.get_service_by_id(service_id, session)
