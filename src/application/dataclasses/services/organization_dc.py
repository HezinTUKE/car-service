from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.enums.services.country import Country


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrganizationDC(DataClassJsonMixin):
    organization_id: str
    name: str
    description: str
    country: Country
    city: str
    street: str
    house_number: str
    postal_code: str
    phone_number: str
    identification_number: str
    email: str
