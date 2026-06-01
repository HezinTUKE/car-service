from enum import StrEnum


class EngineType(StrEnum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    HYBRID_PETROL = "HYBRID_PETROL"
    HYBRID_DIESEL = "HYBRID_DIESEL"
    PHEV_PETROL = "PHEV_PETROL"
    PHEV_DIESEL = "PHEV_DIESEL"
    ELECTRIC = "ELECTRIC"
    LPG = "LPG"
    CNG = "CNG"
