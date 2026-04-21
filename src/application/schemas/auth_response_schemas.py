from pydantic import BaseModel, Field, EmailStr

from application.enums.groups import Groups


class CognitoResponseSchema(BaseModel):
    response: dict


class AuthMethodsResponseSchema(BaseModel):
    access_token: str = ""
    token_type: str = Field(default="bearer")
    success: bool


class ProfileResponseSchema(BaseModel):
    user_id: str
    email: EmailStr
    permissions: list[Groups] = Field(default_factory=list)


class AuthResponseSchema(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str = Field(default="Bearer")
