from pydantic import BaseModel, Field


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")


class SignupResponseSchema(BaseModel):
    result: bool


class LogoutResponseSchema(BaseModel):
    message: str
    user: str | None
