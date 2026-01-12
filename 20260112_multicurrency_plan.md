# Plan: Multi-Currency Support (USD, EUR, GBP)

## Goal
Add multi-currency support to the Budget App, allowing users to track transactions in different currencies and view reports in their preferred currency.

---

## Recommended Approach: Phased Hybrid Implementation

**Phase 1: Display Currency Preference** (Foundation)
- User selects preferred display currency (USD/EUR/GBP)
- All amounts displayed in that currency
- Static exchange rates
- No database schema changes to transaction tables

**Phase 2: Per-Transaction Currency** (Full Multi-Currency)
- Each transaction stores its original currency
- Aggregations convert to user's preferred currency
- Full multi-currency tracking

---

## Phase 1: Display Currency Preference

### Backend Changes

#### 1. Currency Constants
**New file: `backend/app/models/currency.py`**
```python
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP"]
CURRENCY_SYMBOLS = {"USD": "$", "EUR": "€", "GBP": "£"}
```

#### 2. Exchange Rate Service
**New file: `backend/app/services/exchange_rate_service.py`**
- Static exchange rates (USD/EUR/GBP)
- `convert_amount(amount, from_currency, to_currency)` function

#### 3. Auth Router Updates
**File: `backend/app/routers/auth.py`**
- Add `PUT /api/auth/currency` endpoint to update preference
- Enhance `GET /api/auth/status` to return `available_currencies`

#### 4. Schema Updates
**File: `backend/app/schemas/user.py`**
- Add `CurrencyUpdate` schema
- Add `available_currencies` to `UserSettingsResponse`

### Frontend Changes

#### 1. Currency Store
**New file: `frontend/src/lib/stores/currency.ts`**
- Writable store for current currency
- `load()` - fetch from auth status
- `update(currency)` - save preference
- `format(amount)` - format with current currency

#### 2. API Client
**File: `frontend/src/lib/api/client.ts`**
- Add `updateCurrency(currency)` method

#### 3. Replace Hardcoded formatCurrency (7 files)
| File | Current | Change |
|------|---------|--------|
| `routes/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/transactions/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/budgets/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/recurring/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/goals/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/reports/+page.svelte` | Hardcoded USD | Use currency store |
| `routes/banking/+page.svelte` | Hardcoded USD | Use currency store |

#### 4. Settings Page Currency Selector
**File: `frontend/src/routes/settings/+page.svelte`**
- Add "Display Currency" section with dropdown (USD/EUR/GBP)
- Save preference via API

---

## Phase 2: Per-Transaction Currency

### Database Schema Changes

#### Add `currency` column to 6 models:
| Model | File | New Field |
|-------|------|-----------|
| Transaction | `models/transaction.py` | `currency = Column(String, default="USD")` |
| Budget | `models/budget.py` | `currency = Column(String, default="USD")` |
| RecurringTransaction | `models/recurring.py` | `currency = Column(String, default="USD")` |
| Goal | `models/goal.py` | `currency = Column(String, default="USD")` |
| BankConnection | `models/bank.py` | `currency = Column(String, default="USD")` |
| PendingTransaction | `models/bank.py` | `currency = Column(String, default="USD")` |

#### Migration Strategy
- Existing data defaults to USD
- SQLite: recreate tables or use Alembic

### Backend Aggregation Changes

#### Reports Router (`backend/app/routers/reports.py`)
- Monthly summary: Convert each transaction to user's currency before summing
- Category breakdown: Convert before grouping
- Trends: Convert before calculating

#### Budgets Router (`backend/app/routers/budgets.py`)
- Budget status: Convert both budget amount and spent amount to user's currency

#### Goals Router (`backend/app/routers/goals.py`)
- Goal progress: Convert contributions to goal's currency

### Frontend Changes

#### Schema Updates (`frontend/src/lib/api/types.ts`)
- Add `currency` field to Transaction, Budget, Goal, etc.
- Add `converted_amount` for display purposes

#### Transaction Form
- Add currency dropdown (defaults to user's preference)

#### Display Logic
- Show original currency with amount
- Show converted amount in parentheses if different from preference

---

## Critical Files to Modify

### Phase 1 (14 files)
**Backend (7 files):**
1. `backend/app/models/currency.py` (NEW)
2. `backend/app/services/exchange_rate_service.py` (NEW)
3. `backend/app/routers/auth.py`
4. `backend/app/schemas/user.py`
5. `backend/app/models/__init__.py`
6. `backend/app/config.py` (add exchange rate settings)
7. `backend/requirements.txt` (add httpx)

**Frontend (7 files):**
1. `frontend/src/lib/stores/currency.ts` (NEW)
2. `frontend/src/lib/api/client.ts`
3. `frontend/src/lib/api/types.ts`
4. `frontend/src/routes/settings/+page.svelte`
5. `frontend/src/routes/+page.svelte`
6. `frontend/src/routes/transactions/+page.svelte`
7. `frontend/src/routes/budgets/+page.svelte`
8. `frontend/src/routes/recurring/+page.svelte`
9. `frontend/src/routes/goals/+page.svelte`
10. `frontend/src/routes/reports/+page.svelte`
11. `frontend/src/routes/banking/+page.svelte`

### Phase 2 (Additional 15+ files)
- All 6 model files (add currency column)
- All 6 schema files (add currency field)
- 3 router files (reports, budgets, goals - aggregation logic)
- Frontend forms (transaction, budget, goal, recurring)

---

## Exchange Rates

### Rate Provider Options

The exchange rate service will support multiple providers with configurable switching:

| Provider | Type | Cost | Notes |
|----------|------|------|-------|
| **Static** | Built-in | Free | Hardcoded fallback rates |
| **Frankfurter** | Live API | Free | No API key, uses ECB rates, recommended |
| **ExchangeRate-API** | Live API | Free tier | 1,500 req/month, requires API key |
| **Open Exchange Rates** | Live API | Free tier | 1,000 req/month, requires API key |

### Configuration
**File: `backend/app/config.py`**
```python
class Settings(BaseSettings):
    # ... existing settings ...
    exchange_rate_provider: str = "frankfurter"  # "static", "frankfurter", "exchangerate-api"
    exchange_rate_api_key: str | None = None     # Required for some providers
    exchange_rate_cache_minutes: int = 60        # Cache duration
```

### Exchange Rate Service Design
**File: `backend/app/services/exchange_rate_service.py`**

```python
import httpx
from datetime import datetime, timedelta
from app.config import settings

# Static fallback rates
STATIC_RATES = {
    ("USD", "EUR"): 0.92,
    ("USD", "GBP"): 0.79,
    ("EUR", "USD"): 1.09,
    ("EUR", "GBP"): 0.86,
    ("GBP", "USD"): 1.27,
    ("GBP", "EUR"): 1.16,
}

# In-memory cache
_rate_cache = {}
_cache_timestamp = None

async def fetch_live_rates(base: str = "USD") -> dict:
    """Fetch rates from configured provider."""
    if settings.exchange_rate_provider == "frankfurter":
        # Frankfurter API (free, no key required)
        url = f"https://api.frankfurter.app/latest?from={base}&to=EUR,GBP,USD"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            return data.get("rates", {})

    elif settings.exchange_rate_provider == "exchangerate-api":
        # ExchangeRate-API (requires API key)
        url = f"https://v6.exchangerate-api.com/v6/{settings.exchange_rate_api_key}/latest/{base}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            return data.get("conversion_rates", {})

    return {}  # Fall back to static

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Get exchange rate with caching."""
    if from_currency == to_currency:
        return 1.0

    # Check cache first
    cache_key = (from_currency, to_currency)
    if cache_key in _rate_cache:
        return _rate_cache[cache_key]

    # Fall back to static rates
    return STATIC_RATES.get(cache_key, 1.0)

async def refresh_rates():
    """Refresh rates from live provider (call periodically or on-demand)."""
    global _rate_cache, _cache_timestamp

    if settings.exchange_rate_provider == "static":
        _rate_cache = STATIC_RATES.copy()
        return

    # Check if cache is still valid
    if _cache_timestamp and datetime.now() - _cache_timestamp < timedelta(minutes=settings.exchange_rate_cache_minutes):
        return

    try:
        # Fetch rates for each base currency
        for base in ["USD", "EUR", "GBP"]:
            rates = await fetch_live_rates(base)
            for target, rate in rates.items():
                _rate_cache[(base, target)] = rate
        _cache_timestamp = datetime.now()
    except Exception:
        # On error, keep existing cache or use static
        if not _rate_cache:
            _rate_cache = STATIC_RATES.copy()

def convert_amount(amount: float, from_currency: str, to_currency: str) -> float:
    rate = get_exchange_rate(from_currency, to_currency)
    return round(amount * rate, 2)
```

### API Endpoint for Exchange Rates
**File: `backend/app/routers/auth.py`** (or new `currency.py` router)

```python
@router.get("/exchange-rates")
async def get_exchange_rates():
    """Get current exchange rates."""
    await refresh_rates()
    return {
        "provider": settings.exchange_rate_provider,
        "rates": {
            "USD_EUR": get_exchange_rate("USD", "EUR"),
            "USD_GBP": get_exchange_rate("USD", "GBP"),
            "EUR_USD": get_exchange_rate("EUR", "USD"),
            "EUR_GBP": get_exchange_rate("EUR", "GBP"),
            "GBP_USD": get_exchange_rate("GBP", "USD"),
            "GBP_EUR": get_exchange_rate("GBP", "EUR"),
        },
        "cached_at": _cache_timestamp.isoformat() if _cache_timestamp else None
    }

@router.post("/exchange-rates/refresh")
async def refresh_exchange_rates():
    """Force refresh exchange rates from provider."""
    global _cache_timestamp
    _cache_timestamp = None  # Invalidate cache
    await refresh_rates()
    return {"message": "Rates refreshed", "provider": settings.exchange_rate_provider}
```

### Frontend: Display Exchange Rates
**File: `frontend/src/routes/settings/+page.svelte`**
- Show current exchange rates in Settings page
- Add "Refresh Rates" button
- Display rate provider and last updated time

### Dependencies
Add to `backend/requirements.txt`:
```
httpx>=0.27.0
```

---

## Edge Cases

| Case | Solution |
|------|----------|
| Existing data | Default to USD |
| Missing exchange rate | Fall back to static rates |
| User changes preference | Recalculate displays (no DB change in Phase 1) |
| CSV import | Use user's current preference |
| Bank sync | Use bank connection's currency |
| Mixed-currency reports | Convert all to user's preference |
| **Exchange rate API down** | Use cached rates, then fall back to static |
| **API rate limit exceeded** | Cache rates for longer, use static fallback |
| **Network timeout** | Use cached/static rates, log warning |

---

## Verification

### Phase 1 Testing
1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Login and go to Settings
4. Change currency preference to EUR
5. Verify all pages show EUR formatting (€)
6. Change to GBP, verify £ formatting
7. Check Reports page aggregations display correctly

### Phase 2 Testing
1. Create transaction in EUR
2. Create transaction in USD
3. Verify transaction list shows original currencies
4. Verify Reports aggregates in user's preferred currency
5. Test budget with different currency than expenses
6. Test goal contributions in different currencies

---

## Risks

| Risk | Mitigation |
|------|------------|
| Exchange rate volatility | Use static rates for Phase 1; historical rates for Phase 2 |
| Rounding errors | Round to 2 decimal places after conversion |
| Report accuracy | Add disclaimer about converted amounts |
| Data integrity | Never modify original amount/currency |

---

## Implementation Order

### Phase 1 Steps
1. Create `backend/app/models/currency.py`
2. Create `backend/app/services/exchange_rate_service.py`
3. Update `backend/app/schemas/user.py`
4. Update `backend/app/routers/auth.py`
5. Create `frontend/src/lib/stores/currency.ts`
6. Update `frontend/src/lib/api/client.ts`
7. Update `frontend/src/routes/settings/+page.svelte`
8. Replace hardcoded formatCurrency in all 7 route files
9. Test all pages
10. Commit and push

### Phase 2 Steps (after Phase 1 complete)
1. Add currency columns to all models
2. Update all schemas
3. Update aggregation logic in routers
4. Update frontend forms with currency selectors
5. Update display logic for original + converted
6. Comprehensive testing
7. Commit and push
