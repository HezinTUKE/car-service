from dataclasses import dataclass
from dataclasses_json import dataclass_json, DataClassJsonMixin, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class UserPoint(DataClassJsonMixin):
    longitude: float = 0.0
    latitude: float = 0.0
