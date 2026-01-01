from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.enums.services.country import Country
from application.enums.services.currency import Currency
from application.enums.services.metadata import FuncMetadata
from application.enums.services.offer_types import OfferType


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class QuestionMetadataDc(DataClassJsonMixin):
    country: Country | None
    city: str | None
    offer_type: OfferType | None
    func: FuncMetadata | None
    max_price: float | None
    max_distance: float | None
    currency: Currency | None
