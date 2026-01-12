# Utils - CLAUDE.md

> **Location:** `backend/app/utils/`
> **Parent:** [`backend/app/`](../CLAUDE.md)
> **Siblings:** [`models/`](../models/CLAUDE.md), [`schemas/`](../schemas/CLAUDE.md), [`routers/`](../routers/CLAUDE.md), [`services/`](../services/CLAUDE.md)

## Purpose

Shared utility functions for security operations: password hashing and JWT token management.

---

## security.py

### Dependencies

```python
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.config import settings
```

### Password Context

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

Uses bcrypt with automatic salt generation and timing-safe comparison.

---

### Function: `hash_pin(pin: str) -> str`

**Purpose:** Hash plaintext PIN for secure storage

```python
def hash_pin(pin: str) -> str:
    return pwd_context.hash(pin)
```

**Usage:**
```python
from app.utils.security import hash_pin

hashed = hash_pin("1234")  # Store in UserSettings.pin_hash
# Returns: "$2b$12$..." (bcrypt hash string)
```

---

### Function: `verify_pin(plain_pin: str, hashed_pin: str) -> bool`

**Purpose:** Verify PIN against stored hash

```python
def verify_pin(plain_pin: str, hashed_pin: str) -> bool:
    return pwd_context.verify(plain_pin, hashed_pin)
```

**Features:**
- Timing-safe comparison (prevents timing attacks)
- Handles salt automatically

**Usage:**
```python
from app.utils.security import verify_pin

if verify_pin("1234", user.pin_hash):
    # PIN correct - generate token
```

---

### Function: `create_access_token(data: dict) -> str`

**Purpose:** Create JWT access token with expiration

```python
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes  # Default: 10080 (7 days)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.secret_key,      # Default: "change-this-in-production"
        algorithm=settings.algorithm  # Default: "HS256"
    )
```

**Token Payload:**
```python
{
    "sub": "user",     # Subject identifier
    "exp": 1234567890  # Expiration timestamp (auto-added)
}
```

**Usage:**
```python
from app.utils.security import create_access_token

token = create_access_token({"sub": "user"})
return {"access_token": token, "token_type": "bearer"}
```

---

### Function: `verify_token(token: str) -> dict | None`

**Purpose:** Decode and validate JWT token

```python
def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None
```

**Returns:**
- `dict` - Decoded payload if valid
- `None` - If expired, invalid signature, or malformed

**Error Handling:** Catches all `JWTError` variants:
- `ExpiredSignatureError` - Token expired
- `JWTClaimsError` - Invalid claims
- `JWTError` - Malformed/invalid signature

**Usage:**
```python
from app.utils.security import verify_token

payload = verify_token(token_from_header)
if payload:
    user_id = payload.get("sub")  # "user"
else:
    # Return 401 Unauthorized
```

---

## Configuration (from `config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `secret_key` | `"change-this-in-production"` | JWT signing key |
| `algorithm` | `"HS256"` | JWT algorithm |
| `access_token_expire_minutes` | `10080` | Token lifetime (7 days) |

---

## Security Considerations

1. **Secret Key:** MUST be changed in production via environment variable
2. **Token Lifetime:** 7 days is long; consider shorter for production
3. **No Refresh Tokens:** Current implementation lacks token refresh
4. **No Rate Limiting:** Brute-force protection not implemented
5. **PIN Length:** Minimum length not enforced at backend (frontend only)
6. **Token Storage:** Frontend uses localStorage (consider httpOnly cookies)

---

## Used By

| Router | Functions Used |
|--------|----------------|
| `auth.py` | `hash_pin`, `verify_pin`, `create_access_token` |
| *(future)* | `verify_token` for protected routes |

**Note:** Currently, API endpoints do not verify JWT tokens. `verify_token` is available but not used as middleware.
