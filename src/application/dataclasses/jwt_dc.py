from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined

from application.enums.roles import Roles


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class JwtDC:
    username: str
    permission: Roles
    user_id: str
