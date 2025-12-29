from enum import Enum


class RagSource(Enum):
    FILE = "FILE"
    URL = "URL"
    POSTGRESQL = "POSTGRESQL"
    API = "API"
