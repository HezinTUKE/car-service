from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.enums.services.country import Country
from application.enums.services.currency import Currency
from application.enums.services.metadata import FuncMetadata
from application.enums.services.offer_types import OfferType


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class QuestionMetadataDc(DataClassJsonMixin):
    offer_type: OfferType
    country: Country
    city: str | None = None
    func: FuncMetadata | None = None
    max_price: float | None = None
    max_distance: float | None = None
    currency: Currency | None = None
