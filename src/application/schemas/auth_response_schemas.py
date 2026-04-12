from pydantic import BaseModel, Field, EmailStr

from application.enums.roles import Roles


class CognitoResponseSchema(BaseModel):
    response: dict


class AuthMethodsResponseSchema(BaseModel):
    access_token: str = ""
    token_type: str = Field(default="bearer")
    success: bool


class ProfileResponseSchema(BaseModel):
    user_id: str
    email: EmailStr
    permissions: list[Roles] = Field(default_factory=list)


class AuthResponseSchema(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str = Field(default="Bearer")
