from enum import StrEnum


class EngineType(StrEnum):
    EV = "EV"
    ICE = "ICE"


class FuelType(StrEnum):
    DIESEL = "DIESEL"
    PETROL = "PETROL"


class ChargingStandard(StrEnum):
    TYPE1 = "SAE J1772"
    TYPE2 = "IEC 62196 / Mennekes"
    CCS1 = "CCS1"
    CCS2 = "CCS2"
    CHADEMO = "CHAdeMO"
    GBT = "GB/T 20234"
    TESLA = "TESLA Supercharger"
