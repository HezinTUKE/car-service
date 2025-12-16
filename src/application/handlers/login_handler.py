import traceback

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from application.enums.roles import Roles
from application.models import UsersModel
from application.utils.password_utils import create_access_token, hash_password, verify_password


class LoginHandler:

    @classmethod
    async def login(cls, password: str, email: str, session: AsyncSession):
        hashed_password = hash_password(password)
        _query = select(UsersModel).filter(
            UsersModel.email == email
        )
        _query_result = await session.execute(_query)
        user: UsersModel = _query_result.scalar_one_or_none()

        if not user or verify_password(hashed_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        access_token = create_access_token({"sub": user.email})
        refresh_token = create_access_token({"sub": user.email}, True)

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"access_token": access_token, "token_type": "bearer"}
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
        )

        return response

    @classmethod
    async def signup(cls, password: str, email: str, role: Roles, session: AsyncSession):
        try:
            query = select(UsersModel).filter(UsersModel.email == email)
            res = await session.execute(query)
            get_user = res.scalar_one_or_none()

            if get_user:
                raise HTTPException(400, "Email already registered")

            user = UsersModel(email=email, password=hash_password(password), role=role)
            session.add(user)
            return True
        except Exception:
            traceback.print_exc()
            return False