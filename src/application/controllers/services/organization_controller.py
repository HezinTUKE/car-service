import json
from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Body, Form
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import ORGANIZATION_CONTROLLER_PREFIX
from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.enums.groups import Groups
from application.handlers.service_handler.organization_handler import OrganizationHandler
from application.deps.db_deps import get_session
from application.schemas.service_schemas.request_schemas.organization_schema import AddOrganizationRequestSchema
from application.schemas.util_schemas import FilterEntityRequestSchema
from application.schemas.service_schemas.response_schemas.organization_schema import (
    OrganizationResponseSchema,
    OrganizationItemsResponseSchema,
)


class OrganizationController:
    router = APIRouter(prefix=f"/{ORGANIZATION_CONTROLLER_PREFIX}", tags=[ORGANIZATION_CONTROLLER_PREFIX])

    @staticmethod
    @router.post("/create-organization", response_model=OrganizationResponseSchema)
    async def add_organization(
        logo_image: UploadFile,
        current_user: Annotated[JwtDC, Depends(get_current_user)],
        request_schema: str = Form(...),
        session: AsyncSession = Depends(get_session),
    ):
        request_schema = AddOrganizationRequestSchema(**json.loads(request_schema))
        return await OrganizationHandler.create_organization(
            request_schema=request_schema,
            user_id=current_user.user_id,
            logo_file=logo_image,
            session=session
        )

    @staticmethod
    @router.get("/{organization_id}", response_model=OrganizationResponseSchema)
    async def get_organization(
        organization_id: str,
        session: AsyncSession = Depends(get_session),
    ):
        return await OrganizationHandler.get_organization_by_id(organization_id, session)

    @staticmethod
    @router.delete("/remove-organization", response_model=OrganizationResponseSchema)
    async def remove_organization(
        organization_id: str,
        current_user: JwtDC = Depends(get_current_user),
        session: AsyncSession = Depends(get_session),
    ):
        return await OrganizationHandler.remove_organization(organization_id, current_user, session)

    @staticmethod
    @router.get("/get-organizations", response_model=OrganizationItemsResponseSchema)
    async def get_organizations(
        organization_filter: FilterEntityRequestSchema = Depends(),
        session: AsyncSession = Depends(get_session),
    ):
        return await OrganizationHandler.get_list_organizations(organization_filter, session)
