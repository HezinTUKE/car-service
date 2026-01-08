import traceback
import uuid

from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.dataclasses.jwt_dc import JwtDC
from application.enums.roles import Roles
from application.models import UsersModel
from application.schemas.response_schemas import AuthMethodsResponseSchema
from application.utils.password_utils import hash_password, verify_password, get_current_user, set_token
from application.utils.redis_helper import RedisHelper


class LoginHandler:
    @classmethod
    async def login(cls, password: str, email: str, session: AsyncSession):
        hashed_password = hash_password(password)
        _query = select(UsersModel).filter(UsersModel.email == email)
        _query_result = await session.execute(_query)
        user: UsersModel = _query_result.scalar_one_or_none()

        if not user or verify_password(hashed_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        return cls._set_auth_tokens(sub=user.email, permission=user.role, user_id=user.user_id)

    @classmethod
    async def signup(cls, password: str, email: str, role: Roles, session: AsyncSession):
        try:
            query = select(UsersModel).filter(UsersModel.email == email)
            res = await session.execute(query)
            get_user = res.scalar_one_or_none()

            if get_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

            user = UsersModel(email=email, password=hash_password(password), role=role)
            session.add(user)
            return AuthMethodsResponseSchema(success=True)
        except Exception:
            traceback.print_exc()
            return AuthMethodsResponseSchema(success=False)

    @classmethod
    async def logout(cls, request: Request, current_user: JwtDC):
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AuthMethodsResponseSchema(success=True).model_dump(),
        )

        refresh_token = request.cookies.get("refresh_token")
        token_info = get_current_user(refresh_token)

        redis = RedisHelper()
        redis.revoke_token(token_info.jti)

        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return response

    @classmethod
    async def refresh_token(cls, request: Request):
        refresh_cookie = request.cookies.get("refresh_token")
        if not refresh_cookie:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Refresh token missing")

        current_user = get_current_user(refresh_cookie)
        redis = RedisHelper()
        if not redis.check_revoke(current_user.jti):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token has been revoked")

        return cls._set_auth_tokens(
            sub=current_user.username, permission=current_user.permission, user_id=current_user.user_id
        )

    @staticmethod
    def _set_auth_tokens(sub: str, permission: Roles, user_id: str) -> JSONResponse:
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content=AuthMethodsResponseSchema(success=True).model_dump(),
        )

        try:
            set_token(
                response=response,
                data={
                    "sub": sub,
                    "permission": permission.value,
                    "user_id": user_id,
                    "jti": str(uuid.uuid4()),
                },
            )

            set_token(
                response=response,
                data={
                    "sub": sub,
                    "permission": permission.value,
                    "user_id": user_id,
                    "jti": str(uuid.uuid4()),
                },
                refresh_token=True,
            )
        except Exception:
            traceback.print_exc()
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Token generation error")

        return response
