# Lib - CLAUDE.md

> **Location:** `frontend/src/lib/`
> **Parent:** [`frontend/src/`](../CLAUDE.md)
> **Children:** [`api/`](api/CLAUDE.md), [`stores/`](stores/CLAUDE.md)
> **Siblings:** [`routes/`](../routes/CLAUDE.md) (at src level)

## Purpose

Shared library code accessible via the `$lib` import alias. Contains API client, TypeScript types, and reactive stores for global state management.

---

## Directory Structure

```
lib/
├── api/
│   ├── client.ts      # REST API client (38 methods)
│   └── types.ts       # TypeScript interfaces (16 types)
├── stores/
│   ├── auth.ts        # Authentication store (4 methods)
│   └── categories.ts  # Categories store (3 methods)
├── components/        # Empty (UI components inline in routes)
├── assets/
│   └── favicon.svg    # App favicon
└── index.ts           # Empty placeholder
```

---

## Submodules

### api/
REST API communication layer:
- **client.ts** - Singleton `ApiClient` class with all backend endpoints
- **types.ts** - TypeScript interfaces matching Pydantic schemas

### stores/
Svelte reactive stores:
- **auth.ts** - Authentication state (isAuthenticated, isSetup, loading)
- **categories.ts** - Category list with CRUD operations

### components/
Currently empty. UI components are defined directly in route files.

### assets/
Static assets (favicon only currently).

---

## Import Alias

SvelteKit provides the `$lib` alias:

```typescript
// Instead of relative paths
import { api } from '../../../lib/api/client';

// Use $lib alias
import { api } from '$lib/api/client';
import { auth } from '$lib/stores/auth';
import type { Transaction } from '$lib/api/types';
```

---

## Key Exports

### API Client
```typescript
import { api } from '$lib/api/client';

// All endpoints available
await api.getTransactions({ type: 'expense' });
await api.createBudget({ category_id: 1, amount: 500, month: '2026-01' });
await api.syncBankConnection(connectionId);
```

### Stores
```typescript
import { auth } from '$lib/stores/auth';
import { categories } from '$lib/stores/categories';

// Subscribe to state
$: isLoggedIn = $auth.isAuthenticated;

// Call methods
await auth.login(pin);
await categories.load();
```

### Types
```typescript
import type {
  Transaction,
  Category,
  Budget,
  BudgetStatus,
  Goal,
  BankConnection,
  PendingTransaction
} from '$lib/api/types';
```

---

## Data Flow

```
User Action (UI)
    ↓
Store Method / Direct API Call
    ↓
api/client.ts (fetch with JWT)
    ↓
Backend Response
    ↓
Store Update (if applicable)
    ↓
Reactive UI Update ($state / $)
```

---

## Dependencies

```
api/client.ts
    └── fetch (native)
    └── localStorage (token storage)

stores/auth.ts
    └── api/client.ts
    └── svelte/store

stores/categories.ts
    └── api/client.ts
    └── svelte/store
```

---

## Usage Across Routes

| Module | Used By |
|--------|---------|
| `api` | All route pages |
| `auth` store | `+layout.svelte`, `login/+page.svelte` |
| `categories` store | transactions, budgets, recurring, banking, settings pages |
| Types | All pages with TypeScript |
