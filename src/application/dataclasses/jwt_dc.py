from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined

from application.enums.roles import Roles


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class JwtDC:
    username: str
    user_id: str
    jti: str
    permission: Roles | None = None
