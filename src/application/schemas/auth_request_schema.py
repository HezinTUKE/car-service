from pydantic import Field
from pydantic import EmailStr, BaseModel


class AuthRequestSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class ConfirmUserRequestSchema(BaseModel):
    email: EmailStr
    confirmation_code: str = Field(..., min_length=6, max_length=6)


class ResetPasswordRequestSchema(BaseModel):
    email: EmailStr
    confirmation_code: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8, max_length=128)
