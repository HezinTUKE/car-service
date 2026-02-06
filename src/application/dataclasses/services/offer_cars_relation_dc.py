import uuid
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.enums.services.car_brands import CarBrands
from application.enums.services.car_types import CarType
from application.enums.services.country import Country
from application.enums.services.currency import Currency
from application.enums.services.offer_types import OfferType


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OfferCarCompatibilityModelDC(DataClassJsonMixin):
    offer_car_compatibility_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    offer_id: str = ""
    car_type: CarType = field(default=CarBrands.ALL)
    car_brand: CarBrands = field(default=CarType.AMBULANCE)
    created_at: int = None
    updated_at: int = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OfferDC(DataClassJsonMixin):
    offer_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    offer_type: OfferType = field(default=OfferType.CAR_WASH)
    description: str = ""
    currency: Currency = field(default=Currency.EUR)
    base_price: float = 0.0
    sale: int = 0
    service_id: str = ""
    estimated_duration_minutes: int = 1
    created_at: int = None
    updated_at: int = None
    offer_car_compatibility: list[OfferCarCompatibilityModelDC] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ServiceDC(DataClassJsonMixin):
    service_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    name: str = ""
    description: str = ""
    country: Country = field(default=Country.SLOVAKIA)
    city: str = ""
    street: str = ""
    house_number: str = ""
    postal_code: str = ""
    phone_number: str = ""
    email: str = ""
    longitude: float = 0.0
    latitude: float = 0.0
    original_full_address: str = ""
    identification_number: str = ""
    owner: str = ""
    created_at: int = None
    updated_at: int = None
    offers: list[OfferDC] = field(default_factory=list)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class EventData(DataClassJsonMixin):
    services: list[ServiceDC] = field(default_factory=list)
