from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.dataclasses.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.deps.db_deps import get_session
from application.handlers.service_handler.user_handler import UserHandler
from application.schemas.service_schemas.request_schemas.user_setup_schema import CreateUserSetupSchema


class UserController:
    router = APIRouter(prefix="/user", tags=["user"])

    @staticmethod
    @router.post("/create-user-setup")
    async def create_user_setup(
        request: CreateUserSetupSchema,
        current_user: Annotated[JwtDC, Depends(get_current_user)],
        session: Annotated[AsyncSession, Depends(get_session)],
    ):
        return await UserHandler.create_user_setup(
            user_setup=request, user_id=current_user.user_id, session=session
        )
