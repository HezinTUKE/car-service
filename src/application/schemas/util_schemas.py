from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, EmailStr

from application.enums.services.language import LanguageCode
from application.enums.services.country import Country
from application.enums.services.record_status import RecordStatus
from application.schemas.constranits import IdentificationNumber, PhoneNumber


class FilterEntityRequestSchema(BaseModel):
    organization_id: UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: Country | None = Field(default=None)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=4, max_length=20)
    identification_number: IdentificationNumber | None = Field(default=None)
    status: RecordStatus | None = Field(default=RecordStatus.ACTIVE)
    per_page: int = Field(default=10)
    page_num: int = Field(default=1)


class EntityItem(BaseModel):
    name: str
    description: str
    country: Country
    city: str
    street: str
    house_number: str
    postal_code: str
    phone_number: str
    identification_number: str
    longitude: float
    latitude: float
    original_full_address: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class AddressSchema(BaseModel):
    country: Country = Field(default=Country.SLOVAKIA)
    city: str = Field(..., min_length=2, max_length=100)
    street: str = Field(..., min_length=2, max_length=100)
    house_number: str = Field(..., min_length=1, max_length=20)
    postal_code: str = Field(..., min_length=4, max_length=20)


class DescriptionSchema(BaseModel):
    language_code: LanguageCode = Field(LanguageCode.EN, description="Language code for the description, e.g., 'en' for English, 'sk' for Slovak.")
    content: str = Field(..., min_length=10, max_length=120)
