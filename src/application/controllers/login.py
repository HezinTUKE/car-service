from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from application.controllers import LOGIN_CONTROLLER_PREFIX
from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.handlers.login_handler import LoginHandler
from application.models.base import DBModel
from application.schemas.response_schemas import AuthMethodsResponseSchema, ProfileResponseSchema
from application.utils.password_utils import get_current_user


class LoginController:
    router = APIRouter(prefix=f"/{LOGIN_CONTROLLER_PREFIX}", tags=[LOGIN_CONTROLLER_PREFIX])

    @staticmethod
    @router.post(path="/logout", response_model=AuthMethodsResponseSchema)
    async def logout(request: Request, current_user: JwtDC = Depends(get_current_user)):
        return await LoginHandler.logout(request, current_user)

    @staticmethod
    @router.post(path="/signup", response_model=AuthMethodsResponseSchema)
    async def signup(
        email: str,
        password: str,
        role: Roles = Roles.USER,
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        result = await LoginHandler.signup(email=email, password=password, role=role, session=session)
        return {"result": result}

    @staticmethod
    @router.post(path="/signin", response_model=AuthMethodsResponseSchema)
    async def login(
        form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
        session: AsyncSession = Depends(DBModel.get_session),
    ):
        return await LoginHandler.login(password=form_data.password, email=form_data.username, session=session)

    @staticmethod
    @router.post(path="/refresh", response_model=AuthMethodsResponseSchema)
    async def refresh_token(request: Request):
        return await LoginHandler.refresh_token(request)

    @staticmethod
    @router.get(path="/profile", response_model=ProfileResponseSchema)
    async def get_profile(current_user: JwtDC = Depends(get_current_user)):
        return ProfileResponseSchema(
            username=current_user.username, permission=current_user.permission, user_id=current_user.user_id
        )
