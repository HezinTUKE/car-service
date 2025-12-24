from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import SERVICE_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.handlers.service_handler.organization_handler import OrganizationHandler
from application.handlers.service_handler.service_handler import ServiceHandler
from application.models.base import DBModel
from application.schemas.service_schemas.request_schema import (
    AddOrganizationRequestSchema,
    FilterOrganizationRequestSchema,
    AddServiceRequestSchema,
    FilterServiceRequestSchema,
)
from application.schemas.service_schemas.response_schema import (
    ManipulateOrganizationResponseSchema,
    OrganizationItemsResponseSchema,
    ManipulateServiceResponseSchema,
    ServiceItemsResponseSchema,
)
from application.utils.password_utils import permission_required


class ServiceController:
    router = APIRouter(prefix=f"/{SERVICE_CONTROLLER_PREFIX}", tags=[SERVICE_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/add-organization", response_model=ManipulateOrganizationResponseSchema)
    async def add_organization(
        request_schema: AddOrganizationRequestSchema = Body(...),
        current_user: JwtDC = Depends(permission_required((Roles.MASTER, Roles.USER))),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await OrganizationHandler.add_organization(request_schema, current_user.user_id, session)

    @staticmethod
    @router.delete("/remove-organization", response_model=ManipulateOrganizationResponseSchema)
    async def remove_organization(
        organization_id: str,
        current_user: JwtDC = Depends(permission_required((Roles.MASTER, Roles.USER))),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        res = await OrganizationHandler.remove_organization(organization_id, current_user, session)
        return {"status": res}

    @staticmethod
    @router.get("/get-organizations", response_model=OrganizationItemsResponseSchema)
    async def get_organizations(
        organization_filter: FilterOrganizationRequestSchema = Depends(),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await OrganizationHandler.get_organizations(organization_filter, session)

    @staticmethod
    @router.post("/add-service", response_model=ManipulateServiceResponseSchema)
    async def add_service(
        request_schema: AddServiceRequestSchema,
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
        return await OrganizationHandler.get_services(service_filter, session)
