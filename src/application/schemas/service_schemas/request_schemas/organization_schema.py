from pydantic import BaseModel, Field, EmailStr

from application.enums.services.country import Country
from application.schemas.util_schemas import PhoneNumber, IdentificationNumber


class AddOrganizationRequestSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=10)
    country: Country = Field(default=Country.SLOVAKIA)
    city: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=2, max_length=100)
    house_number: str = Field(..., min_length=1, max_length=20)
    postal_code: str = Field(..., min_length=4, max_length=20)
    phone_number: PhoneNumber
    identification_number: IdentificationNumber
    email: EmailStr


