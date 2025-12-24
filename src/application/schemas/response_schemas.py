from pydantic import BaseModel, Field

from application.enums.roles import Roles


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class SignupResponseSchema(BaseModel):
    result: bool


class LogoutResponseSchema(BaseModel):
    message: str
    user: str | None
    permission: Roles
