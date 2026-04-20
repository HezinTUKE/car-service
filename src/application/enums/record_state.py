from enum import StrEnum


class RecordState(StrEnum):
    ACTIVE = 'ACTIVE'
    ARCHIVED = 'ARCHIVED'
    PENDING = 'PENDING'
