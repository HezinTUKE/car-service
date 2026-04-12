from typing import Annotated

from pydantic import StringConstraints

PhoneNumber = Annotated[str, StringConstraints(min_length=7, max_length=20, pattern=r"^\+?[1-9]\d{1,14}$")]
IdentificationNumber = Annotated[str, StringConstraints(min_length=5, max_length=50, pattern=r"^[A-Za-z0-9\-]+$")]
