"""Exchange rate service with multiple provider support and caching."""

import httpx
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
from app.config import settings
from app.models.currency import SUPPORTED_CURRENCIES


# Static fallback rates (approximate rates as of 2026)
STATIC_RATES: Dict[Tuple[str, str], float] = {
    ("USD", "EUR"): 0.92,
    ("USD", "GBP"): 0.79,
    ("EUR", "USD"): 1.09,
    ("EUR", "GBP"): 0.86,
    ("GBP", "USD"): 1.27,
    ("GBP", "EUR"): 1.16,
}

# In-memory cache
_rate_cache: Dict[Tuple[str, str], float] = {}
_cache_timestamp: Optional[datetime] = None


async def fetch_frankfurter_rates(base: str = "USD") -> Dict[str, float]:
    """Fetch rates from Frankfurter API (free, no API key required)."""
    targets = ",".join([c for c in SUPPORTED_CURRENCIES if c != base])
    url = f"https://api.frankfurter.app/latest?from={base}&to={targets}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("rates", {})


async def fetch_exchangerate_api_rates(base: str = "USD") -> Dict[str, float]:
    """Fetch rates from ExchangeRate-API (requires API key)."""
    if not settings.exchange_rate_api_key:
        raise ValueError("exchange_rate_api_key is required for exchangerate-api provider")

    url = f"https://v6.exchangerate-api.com/v6/{settings.exchange_rate_api_key}/latest/{base}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            raise ValueError(f"API error: {data.get('error-type', 'unknown')}")

        # Filter to only supported currencies
        all_rates = data.get("conversion_rates", {})
        return {k: v for k, v in all_rates.items() if k in SUPPORTED_CURRENCIES}


async def fetch_live_rates(base: str = "USD") -> Dict[str, float]:
    """Fetch rates from configured provider."""
    if settings.exchange_rate_provider == "frankfurter":
        return await fetch_frankfurter_rates(base)
    elif settings.exchange_rate_provider == "exchangerate-api":
        return await fetch_exchangerate_api_rates(base)
    else:
        return {}


def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate with caching. Synchronous version using cached data."""
    if from_currency == to_currency:
        return 1.0

    # Validate currencies
    if from_currency not in SUPPORTED_CURRENCIES or to_currency not in SUPPORTED_CURRENCIES:
        return 1.0

    # Check cache first
    cache_key = (from_currency, to_currency)
    if cache_key in _rate_cache:
        return _rate_cache[cache_key]

    # Fall back to static rates
    return STATIC_RATES.get(cache_key, 1.0)


async def refresh_rates() -> bool:
    """
    Refresh rates from live provider.
    Returns True if rates were successfully refreshed, False otherwise.
    """
    global _rate_cache, _cache_timestamp

    # Use static rates if provider is set to static
    if settings.exchange_rate_provider == "static":
        _rate_cache = STATIC_RATES.copy()
        _cache_timestamp = datetime.now()
        return True

    # Check if cache is still valid
    cache_duration = timedelta(minutes=settings.exchange_rate_cache_minutes)
    if _cache_timestamp and datetime.now() - _cache_timestamp < cache_duration:
        return True  # Cache still valid

    try:
        # Fetch rates for each base currency
        new_cache: Dict[Tuple[str, str], float] = {}

        for base in SUPPORTED_CURRENCIES:
            rates = await fetch_live_rates(base)
            for target, rate in rates.items():
                if target != base:
                    new_cache[(base, target)] = rate

        if new_cache:
            _rate_cache = new_cache
            _cache_timestamp = datetime.now()
            return True
        else:
            # No rates fetched, keep existing or use static
            if not _rate_cache:
                _rate_cache = STATIC_RATES.copy()
            return False

    except Exception as e:
        # On error, keep existing cache or use static as fallback
        print(f"Warning: Failed to fetch exchange rates: {e}")
        if not _rate_cache:
            _rate_cache = STATIC_RATES.copy()
            _cache_timestamp = datetime.now()
        return False


def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount between currencies."""
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)


def get_all_rates() -> Dict[str, float]:
    """Get all cached exchange rates."""
    result = {}
    for (from_curr, to_curr), rate in _rate_cache.items():
        result[f"{from_curr}_{to_curr}"] = rate

    # Add static rates if cache is empty
    if not result:
        for (from_curr, to_curr), rate in STATIC_RATES.items():
            result[f"{from_curr}_{to_curr}"] = rate

    return result


def get_cache_info() -> Dict:
    """Get cache status information."""
    return {
        "provider": settings.exchange_rate_provider,
        "cached_at": _cache_timestamp.isoformat() if _cache_timestamp else None,
        "cache_duration_minutes": settings.exchange_rate_cache_minutes,
        "rates_count": len(_rate_cache),
    }


def invalidate_cache():
    """Force cache invalidation for next refresh."""
    global _cache_timestamp
    _cache_timestamp = None
