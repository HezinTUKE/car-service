from dataclasses import dataclass,  field

from dataclasses_json import dataclass_json, Undefined, DataClassJsonMixin

from application.enums.groups import Groups


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class JwtDC(DataClassJsonMixin):
    user_id: str
    token_type: str
    token: str
    email: str | None = None
    role: list[Groups] = field(default_factory=list)
