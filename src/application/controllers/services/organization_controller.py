from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import ORGANIZATION_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.handlers.service_handler.organization_handler import OrganizationHandler
from application.models.base import DBModel
from application.schemas.service_schemas.request_schemas.organization_schema import AddOrganizationRequestSchema
from application.schemas.util_schemas import FilterEntityRequestSchema
from application.schemas.service_schemas.response_schemas.organization_schema import \
    ManipulateOrganizationResponseSchema, OrganizationItemsResponseSchema
from application.utils.password_utils import permission_required


class OrganizationController:
    router = APIRouter(prefix=f"/{ORGANIZATION_CONTROLLER_PREFIX}", tags=[ORGANIZATION_CONTROLLER_PREFIX])

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
        organization_filter: FilterEntityRequestSchema = Depends(),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await OrganizationHandler.get_organizations(organization_filter, session)
