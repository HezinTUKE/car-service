from typing import Annotated

from fastapi import APIRouter, Depends, Body
from application.controllers import LOGIN_CONTROLLER_PREFIX
from application.dto.jwt_dc import JwtDC
from application.deps.auth_deps import get_current_user
from application.handlers.login_handler import LoginHandler
from application.schemas.auth_request_schema import AuthRequestSchema, ConfirmUserRequestSchema, \
    ResetPasswordRequestSchema
from application.schemas.auth_response_schemas import AuthResponseSchema, CognitoResponseSchema, ProfileResponseSchema


class LoginController:
    router = APIRouter(prefix=f"/{LOGIN_CONTROLLER_PREFIX}", tags=[LOGIN_CONTROLLER_PREFIX])

    @staticmethod
    @router.post(
        path="/signup",
        response_model=CognitoResponseSchema,
    )
    async def signup(
        request: AuthRequestSchema
    ):
        result = await LoginHandler.signup(request)
        return result

    @staticmethod
    @router.post(
        path="/confirm-email",
        response_model=CognitoResponseSchema,
    )
    async def confirm_email(
        request: ConfirmUserRequestSchema
    ):
        result = await LoginHandler.confirm_email(request)
        return result

    @staticmethod
    @router.post(
        path="/signin",
        response_model=AuthResponseSchema,
    )
    async def login(request: AuthRequestSchema):
        result = await LoginHandler.login(request)
        return result

    @staticmethod
    @router.post(
        path="/logout",
        response_model=CognitoResponseSchema,
    )
    async def logout(
        current_user: Annotated[JwtDC, Depends(get_current_user)],
    ):
        return await LoginHandler.logout(current_user.token)

    @staticmethod
    @router.post(
        path="/refresh",
        response_model=AuthResponseSchema,
    )
    async def refresh_token(
        current_user: Annotated[JwtDC, Depends(get_current_user)],
        refresh_token: str = Body(..., embed=True),
    ):
        return await LoginHandler.refresh_token(refresh_token, current_user.email)

    @staticmethod
    @router.post(
        path="/forgot-password",
        response_model=CognitoResponseSchema,
    )
    async def forgot_password(
        email : str = Body(..., embed=True),
    ):
        return await LoginHandler.forgot_password(email)

    @staticmethod
    @router.post(
        path="/reset-password",
        response_model=CognitoResponseSchema,
    )
    async def reset_password(
        request: ResetPasswordRequestSchema
    ):
        return await LoginHandler.reset_password(
            email=str(request.email),
            confirmation_code=request.confirmation_code,
            new_password=request.new_password
        )

    @staticmethod
    @router.get(
        path="/profile",
        response_model=ProfileResponseSchema
    )
    async def get_current_user_info(
        current_user: Annotated[JwtDC, Depends(get_current_user)],
    ):
        return ProfileResponseSchema(
            user_id=current_user.user_id,
            email=current_user.email,
            permissions=current_user.groups
        )
