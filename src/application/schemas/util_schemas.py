from typing_extensions import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, StringConstraints

from application.enums.services.country import Country


PhoneNumber = Annotated[str, StringConstraints(min_length=7, max_length=20, pattern=r"^\+?[1-9]\d{1,14}$")]
IdentificationNumber = Annotated[str, StringConstraints(min_length=5, max_length=50, pattern=r"^[A-Za-z0-9\-]+$")]


class FilterEntityRequestSchema(BaseModel):
    organization_id: UUID | None = Field(default=None)
    name: str | None = Field(default=None, min_length=2, max_length=100)
    country: Country | None = Field(default=None)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    postal_code: str | None = Field(default=None, min_length=4, max_length=20)
    identification_number: IdentificationNumber | None = Field(default=None)
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
