# Utils - CLAUDE.md

## Overview

Shared utility functions for security operations including password hashing and JWT token management.

## security.py

### Password Hashing

Uses `passlib` with bcrypt algorithm for secure PIN storage.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

**Functions:**

`hash_pin(pin: str) -> str`
- Hashes plaintext PIN using bcrypt
- Returns hash string for database storage
- Automatically handles salt generation

`verify_pin(plain_pin: str, hashed_pin: str) -> bool`
- Compares plaintext PIN against stored hash
- Uses timing-safe comparison to prevent timing attacks
- Returns True if match, False otherwise

**Usage:**
```python
from app.utils.security import hash_pin, verify_pin

# Storing a PIN
hashed = hash_pin("1234")
# Store hashed in database

# Verifying a PIN
if verify_pin("1234", hashed):
    print("PIN correct")
```

### JWT Token Management

Uses `python-jose` for JSON Web Token creation and verification.

**Configuration (from config.py):**
- Algorithm: HS256
- Expiration: 7 days (10080 minutes)
- Secret Key: Configured via environment variable

`create_access_token(data: dict) -> str`
- Creates JWT with provided payload
- Adds expiration timestamp automatically
- Signs with configured secret key and algorithm

`verify_token(token: str) -> dict | None`
- Decodes and validates JWT
- Returns payload dict if valid
- Returns None on any error (expired, invalid signature, malformed)

**Token Payload:**
```python
{
    "sub": "user",     # Subject (user identifier)
    "exp": 1234567890  # Expiration timestamp
}
```

**Usage:**
```python
from app.utils.security import create_access_token, verify_token

# Creating a token
token = create_access_token({"sub": "user"})

# Verifying a token
payload = verify_token(token)
if payload:
    print(f"Valid token for: {payload['sub']}")
else:
    print("Invalid or expired token")
```

## Dependencies

Required packages in `requirements.txt`:
- `passlib[bcrypt]` - Password hashing
- `bcrypt<5.0.0` - Bcrypt implementation (pinned for compatibility)
- `python-jose[cryptography]` - JWT handling

## Security Notes

1. **Secret Key**: Must be changed from default in production
2. **Token Storage**: Frontend stores in localStorage (consider httpOnly cookies for production)
3. **PIN Requirements**: Minimum 4 characters enforced at frontend
4. **No Rate Limiting**: Consider adding for production brute-force protection
