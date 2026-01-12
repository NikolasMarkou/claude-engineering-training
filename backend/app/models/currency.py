"""Currency constants and supported currencies for multi-currency support."""

from enum import Enum


class Currency(str, Enum):
    """Supported currencies."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP"]

CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
}

CURRENCY_NAMES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
}

CURRENCY_LOCALES = {
    "USD": "en-US",
    "EUR": "de-DE",
    "GBP": "en-GB",
}
