from pydantic import BaseModel, Field

from application.enums.roles import Roles


class AuthMethodsResponseSchema(BaseModel):
    access_token: str = ""
    token_type: str = Field(default="bearer")
    success: bool


class ProfileResponseSchema(BaseModel):
    username: str
    user_id: str
    permission: Roles = Field(default=Roles.USER)
