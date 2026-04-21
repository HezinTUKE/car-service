from loguru import logger

from application.enums.groups import Groups
from application.schemas.auth_request_schema import AuthRequestSchema, ConfirmUserRequestSchema
from application.schemas.auth_response_schemas import CognitoResponseSchema, AuthResponseSchema
from application.utils.cognito_service import CognitoService
from application.utils.exceptions import BadRequestException


class LoginHandler:
    @classmethod
    async def signup(cls, request: AuthRequestSchema):
        try:
            repo = CognitoService()
            response = repo.sign_up_user(request.password, str(request.email))
            repo.add_user_to_group(username=str(request.email), group_name=Groups.USER)
            return CognitoResponseSchema(response=response)
        except Exception as e:
            logger.exception("Error registering user", exc_info=True)
            raise BadRequestException(detail=str(e))

    @classmethod
    async def confirm_email(cls, request: ConfirmUserRequestSchema):
        try:
            repo = CognitoService()
            response = repo.confirm_user(str(request.email), request.confirmation_code)
            return CognitoResponseSchema(response=response)
        except Exception:
            logger.exception("Error confirming user", exc_info=True)
            raise BadRequestException()

    @classmethod
    async def login(cls, request: AuthRequestSchema):
        try:
            repo = CognitoService()
            return repo.login_user(str(request.email), request.password)
        except Exception as e:
            logger.exception("Error logging in user", exc_info=True)
            raise BadRequestException(detail=str(e))

    @classmethod
    async def forgot_password(cls, email: str):
        try:
            repo = CognitoService()
            response = repo.forgot_password(email)
            return CognitoResponseSchema(response=response)
        except Exception as e:
            logger.exception("Error initiating forgot password flow", exc_info=True)
            raise BadRequestException(detail=str(e))

    @classmethod
    async def reset_password(cls, email: str, new_password: str, confirmation_code: str):
        try:
            repo = CognitoService()
            response = repo.reset_password(username=email, new_password=new_password, confirmation_code=confirmation_code)
            return CognitoResponseSchema(response=response)
        except Exception as e:
            logger.exception("Error resetting password", exc_info=True)
            raise BadRequestException(detail=str(e))

    @classmethod
    async def refresh_token(cls, refresh_token: str, current_user: str):
        if not current_user:
            raise BadRequestException(detail="User not authenticated")

        try:
            repo = CognitoService()
            token = repo.refresh_token(refresh_token)
            return token
        except Exception:
            logger.exception("Error refreshing token", exc_info=True)
            raise BadRequestException("Failed to refresh token")

    @classmethod
    async def logout(cls, access_token: str):
        if not access_token:
            raise BadRequestException(detail="User not authenticated")

        try:
            repo = CognitoService()
            response = repo.logout_user(access_token)
            return CognitoResponseSchema(response=response)
        except Exception:
            logger.exception("Error logging out user", exc_info=True)
            raise BadRequestException("Failed to log out user")
