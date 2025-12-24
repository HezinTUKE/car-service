from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import LOGIN_CONTROLLER_PREFIX
from application.enums.roles import Roles
from application.handlers.login_handler import LoginHandler
from application.models.base import DBModel
from application.schemas.response_schemas import (
    LoginResponseSchema,
    SignupResponseSchema,
    LogoutResponseSchema,
)
from application.utils.password_utils import get_current_user


class LoginController:
    router = APIRouter(prefix=f"/{LOGIN_CONTROLLER_PREFIX}", tags=[LOGIN_CONTROLLER_PREFIX])

    @staticmethod
    @router.post(path="/logout", response_model=LogoutResponseSchema)
    async def logout(current_user: tuple[str, str] = Depends(get_current_user)):
        user, permission = current_user
        await LoginHandler.logout()
        return {"message": "Access granted", "user": user, "permission": permission}

    @staticmethod
    @router.post(path="/signup", response_model=SignupResponseSchema)
    async def signup(
        email: str,
        password: str,
        role: Roles = Roles.USER,
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        result = await LoginHandler.signup(email=email, password=password, role=role, session=session)
        return {"result": result}

    @staticmethod
    @router.post(path="/signin", response_model=LoginResponseSchema)
    async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await LoginHandler.login(password=form_data.password, email=form_data.username, session=session)
