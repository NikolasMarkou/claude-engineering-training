# API - CLAUDE.md

## Overview

REST API client and TypeScript type definitions for communicating with the FastAPI backend.

## Files

### client.ts - API Client

Singleton class handling all backend communication.

**Configuration:**
- Base URL: `http://localhost:8000/api`
- Token Storage: localStorage (`budget_token`)
- Auth Header: `Authorization: Bearer {token}`

**Token Management:**
```typescript
api.setToken(token: string)  // Store token
api.clearToken()             // Remove token
api.isAuthenticated()        // Check if token exists
```

**Authentication Endpoints:**
```typescript
api.getAuthStatus()                        // GET /auth/status
api.setupPin(pin: string)                  // POST /auth/setup
api.login(pin: string)                     // POST /auth/login
api.changePin(currentPin, newPin)          // POST /auth/change-pin
```

**Transaction Endpoints:**
```typescript
api.getTransactions(filters?)              // GET /transactions
api.createTransaction(data)                // POST /transactions
api.updateTransaction(id, data)            // PUT /transactions/{id}
api.deleteTransaction(id)                  // DELETE /transactions/{id}
```

**Category Endpoints:**
```typescript
api.getCategories()                        // GET /categories
api.createCategory(data)                   // POST /categories
api.deleteCategory(id)                     // DELETE /categories/{id}
```

**Budget Endpoints:**
```typescript
api.getBudgets(month)                      // GET /budgets?month=YYYY-MM
api.createBudget(data)                     // POST /budgets
api.getBudgetStatus(month)                 // GET /budgets/status?month=YYYY-MM
api.deleteBudget(id)                       // DELETE /budgets/{id}
```

**Recurring Transaction Endpoints:**
```typescript
api.getRecurringTransactions()             // GET /recurring
api.createRecurringTransaction(data)       // POST /recurring
api.updateRecurringTransaction(id, data)   // PUT /recurring/{id}
api.deleteRecurringTransaction(id)         // DELETE /recurring/{id}
api.processRecurringTransactions()         // POST /recurring/process
```

**Goal Endpoints:**
```typescript
api.getGoals()                             // GET /goals
api.createGoal(data)                       // POST /goals
api.updateGoal(id, data)                   // PUT /goals/{id}
api.contributeToGoal(id, amount)           // POST /goals/{id}/contribute
api.deleteGoal(id)                         // DELETE /goals/{id}
```

**Report Endpoints:**
```typescript
api.getMonthlySummary(month)               // GET /reports/monthly-summary
api.getCategoryBreakdown(month)            // GET /reports/category-breakdown
api.getTrends(months)                      // GET /reports/trends?months=N
```

**Import Endpoints:**
```typescript
api.uploadCSV(file: File)                  // POST /import/csv
api.confirmImport(rows)                    // POST /import/confirm
```

**Banking Endpoints:**
```typescript
api.getAvailableBanks()                    // GET /banking/banks
api.getBankConnections()                   // GET /banking/connections
api.createBankConnection(data)             // POST /banking/connections
api.deleteBankConnection(id)               // DELETE /banking/connections/{id}
api.syncBankConnection(id)                 // POST /banking/connections/{id}/sync
api.getPendingTransactions()               // GET /banking/pending
api.importPendingTransaction(id, catId)    // POST /banking/pending/{id}/import
api.dismissPendingTransaction(id)          // POST /banking/pending/{id}/dismiss
api.importAllPending()                     // POST /banking/pending/import-all
api.getBankBalances()                      // GET /banking/balances
```

### types.ts - TypeScript Interfaces

**Core Types:**
```typescript
interface Category {
  id: number;
  name: string;
  type: 'income' | 'expense';
  is_default: boolean;
  icon: string | null;
  color: string | null;
}

interface Transaction {
  id: number;
  amount: number;
  type: 'income' | 'expense';
  category_id: number;
  category: Category;
  description: string | null;
  date: string;
}

interface Budget {
  id: number;
  category_id: number;
  category: Category;
  amount: number;
  month: string;
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
  category: Category;
  description: string | null;
  frequency: 'daily' | 'weekly' | 'monthly';
  next_run_date: string;
  is_active: boolean;
}

interface Goal {
  id: number;
  name: string;
  target_amount: number;
  current_amount: number;
  deadline: string;
  progress_percentage: number;
  days_remaining: number;
}

interface BankConnection {
  id: number;
  bank_name: string;
  account_name: string;
  account_type: string;
  balance: number;
  last_synced: string | null;
  is_active: boolean;
}

interface PendingTransaction {
  id: number;
  bank_connection_id: number;
  external_id: string;
  amount: number;
  merchant_name: string;
  date: string;
  suggested_category_id: number | null;
  suggested_category: Category | null;
  status: 'pending' | 'imported' | 'dismissed';
}
```

## Error Handling

The client parses JSON error responses:

```typescript
try {
  await api.createTransaction(data);
} catch (error) {
  // error.message contains backend error detail
  console.error(error.message);
}
```

## Usage Example

```typescript
import { api } from '$lib/api/client';
import type { Transaction } from '$lib/api/types';

// In a Svelte component
let transactions: Transaction[] = $state([]);

async function loadTransactions() {
  transactions = await api.getTransactions({
    start_date: '2026-01-01',
    type: 'expense'
  });
}
```
