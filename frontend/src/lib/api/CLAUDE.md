# API Client - CLAUDE.md

> **Location:** `frontend/src/lib/api/`
> **Parent:** [`frontend/src/lib/`](../CLAUDE.md)
> **Siblings:** [`stores/`](../stores/CLAUDE.md)

## Purpose

REST API client and TypeScript type definitions for communicating with the FastAPI backend. Provides type-safe HTTP requests with automatic JWT token management.

---

## Files

| File | Purpose |
|------|---------|
| `client.ts` | Singleton API client class (38 methods) |
| `types.ts` | TypeScript interfaces (16 types) |

---

## client.ts - API Client

### Configuration

```typescript
const BASE_URL = 'http://localhost:8000/api';
```

Token stored in `localStorage` with key `'token'`.

### Token Management

| Method | Signature | Purpose |
|--------|-----------|---------|
| `setToken` | `(token: string) => void` | Store JWT in memory + localStorage |
| `clearToken` | `() => void` | Remove token from memory + localStorage |
| `isAuthenticated` | `() => boolean` | Check if token exists |

### Core Request Handler

```typescript
private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T>
```

- Adds `Content-Type: application/json`
- Adds `Authorization: Bearer {token}` if authenticated
- Throws `Error` with parsed detail on non-2xx responses
- Returns `undefined` for 204 No Content

### Authentication Endpoints (4)

| Method | HTTP | Path | Request | Response |
|--------|------|------|---------|----------|
| `getAuthStatus()` | GET | `/auth/status` | - | `AuthStatus` |
| `setupPin(pin)` | POST | `/auth/setup` | `{pin}` | `Token` |
| `login(pin)` | POST | `/auth/login` | `{pin}` | `Token` |
| `changePin(currentPin, newPin)` | POST | `/auth/change-pin` | `{current_pin, new_pin}` | void |

### Transaction Endpoints (4)

| Method | HTTP | Path | Parameters | Response |
|--------|------|------|------------|----------|
| `getTransactions(params?)` | GET | `/transactions` | `start_date?, end_date?, category_id?, type?` | `Transaction[]` |
| `createTransaction(data)` | POST | `/transactions` | `TransactionCreate` | `Transaction` |
| `updateTransaction(id, data)` | PUT | `/transactions/{id}` | `Partial<TransactionCreate>` | `Transaction` |
| `deleteTransaction(id)` | DELETE | `/transactions/{id}` | - | void |

### Category Endpoints (3)

| Method | HTTP | Path | Response |
|--------|------|------|----------|
| `getCategories()` | GET | `/categories` | `Category[]` |
| `createCategory(data)` | POST | `/categories` | `Category` |
| `deleteCategory(id)` | DELETE | `/categories/{id}` | void |

### Budget Endpoints (4)

| Method | HTTP | Path | Parameters | Response |
|--------|------|------|------------|----------|
| `getBudgets(month)` | GET | `/budgets?month=` | `YYYY-MM` | `Budget[]` |
| `createBudget(data)` | POST | `/budgets` | `{category_id, amount, month}` | `Budget` |
| `getBudgetStatus(month)` | GET | `/budgets/status?month=` | `YYYY-MM` | `BudgetStatus[]` |
| `deleteBudget(id)` | DELETE | `/budgets/{id}` | - | void |

### Recurring Transaction Endpoints (5)

| Method | HTTP | Path | Response |
|--------|------|------|----------|
| `getRecurring()` | GET | `/recurring` | `RecurringTransaction[]` |
| `createRecurring(data)` | POST | `/recurring` | `RecurringTransaction` |
| `updateRecurring(id, data)` | PUT | `/recurring/{id}` | `RecurringTransaction` |
| `deleteRecurring(id)` | DELETE | `/recurring/{id}` | void |
| `processRecurring()` | POST | `/recurring/process` | `{processed: number}` |

### Goal Endpoints (5)

| Method | HTTP | Path | Response |
|--------|------|------|----------|
| `getGoals()` | GET | `/goals` | `Goal[]` |
| `createGoal(data)` | POST | `/goals` | `Goal` |
| `updateGoal(id, data)` | PUT | `/goals/{id}` | `Goal` |
| `contributeToGoal(id, amount)` | POST | `/goals/{id}/contribute` | `Goal` |
| `deleteGoal(id)` | DELETE | `/goals/{id}` | void |

### Report Endpoints (3)

| Method | HTTP | Path | Response |
|--------|------|------|----------|
| `getMonthlySummary(month)` | GET | `/reports/monthly-summary?month=` | `MonthlySummary` |
| `getCategoryBreakdown(month)` | GET | `/reports/category-breakdown?month=` | `CategoryBreakdown[]` |
| `getTrends(months?)` | GET | `/reports/trends?months=` | `MonthlySummary[]` |

### Import Endpoints (2)

| Method | HTTP | Path | Note |
|--------|------|------|------|
| `uploadCSV(file)` | POST | `/import/csv` | Uses FormData |
| `confirmImport(rows)` | POST | `/import/confirm` | JSON body |

### Banking Endpoints (10)

| Method | HTTP | Path | Response |
|--------|------|------|----------|
| `getAvailableBanks()` | GET | `/banking/banks` | `BankInfo[]` |
| `getBankConnections()` | GET | `/banking/connections` | `BankConnection[]` |
| `createBankConnection(data)` | POST | `/banking/connections` | `BankConnection` |
| `deleteBankConnection(id)` | DELETE | `/banking/connections/{id}` | void |
| `syncBankConnection(id)` | POST | `/banking/connections/{id}/sync` | `{synced, balance}` |
| `getPendingTransactions()` | GET | `/banking/pending` | `PendingTransaction[]` |
| `importPendingTransaction(id, categoryId)` | POST | `/banking/pending/{id}/import` | `{message, transaction_id}` |
| `dismissPendingTransaction(id)` | POST | `/banking/pending/{id}/dismiss` | void |
| `importAllPending()` | POST | `/banking/pending/import-all` | `{imported}` |
| `getBankBalances()` | GET | `/banking/balances` | `BankBalance[]` |

---

## types.ts - TypeScript Interfaces

### Core Types

```typescript
interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  is_default: boolean;
  icon: string | null;
  color: string | null;
  created_at: string;
}

interface Transaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string | null;
  date: string;
  created_at: string;
  category: Category;  // Nested
}

interface Budget {
  id: number;
  category_id: number;
  amount: number;
  month: string;  // YYYY-MM
  created_at: string;
  category: Category;  // Nested
}

interface BudgetStatus {
  category_id: number;
  category_name: string;
  budgeted: number;
  spent: number;
  remaining: number;
  percentage_used: number;
}

interface RecurringTransaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  description: string | null;
  frequency: 'daily' | 'weekly' | 'monthly';
  next_run_date: string;
  is_active: boolean;
  created_at: string;
  category: Category;  // Nested
}

interface Goal {
  id: number;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  created_at: string;
  progress_percentage: number;  // Computed
  days_remaining: number;       // Computed
}
```

### Banking Types

```typescript
interface BankInfo {
  name: string;
  accounts: string[];
}

interface BankConnection {
  id: number;
  bank_name: string;
  account_name: string;
  account_type: string;
  balance: number;
  last_synced: string | null;
  is_active: boolean;
  created_at: string;
}

interface PendingTransaction {
  id: number;
  bank_connection_id: number;
  external_id: string;
  amount: number;
  merchant_name: string;
  date: string;
  suggested_category_id: number | null;
  suggested_category: Category | null;  // Nested optional
  status: string;
  created_at: string;
}
```

### Auth Types

```typescript
interface AuthStatus {
  currency: string;
  is_setup: boolean;
}

interface Token {
  access_token: string;
  token_type: string;
}
```

---

## Usage Example

```typescript
import { api } from '$lib/api/client';
import type { Transaction } from '$lib/api/types';

// In a Svelte component
let transactions: Transaction[] = $state([]);

async function loadData() {
  transactions = await api.getTransactions({
    start_date: '2026-01-01',
    type: 'expense'
  });
}
```

---

## Error Handling

```typescript
try {
  await api.createTransaction(data);
} catch (error) {
  // error.message contains backend error detail
  console.error(error.message);
}
```
