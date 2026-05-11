from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, DataClassJsonMixin, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ProductDC(DataClassJsonMixin):
    id: str
    object: str
    active: bool
    created: int
    default_price: int | None
    description: str | None
    updated: int
    images: list[dict] = field(default_factory=list)
    marketing_features: list[dict] = field(default_factory=list)
    livemode: bool = False
    metadata: dict[str, str] = field(default_factory=dict)
    shippable: bool | None = None
    statement_descriptor: str | None = None
    tax_code: str | None = None
    unit_label: str | None = None
    url: str | None = None
