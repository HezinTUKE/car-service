from enum import Enum


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"
    GBP = "GBP"
    CZK = "CZK"
    HUF = "HUF"
