# Lib - CLAUDE.md

## Overview

Shared library code accessible via the `$lib` import alias. Contains API client, TypeScript types, reactive stores, and reusable components.

## Subdirectories

### api/
API communication layer:
- `client.ts` - REST API client class with all endpoints
- `types.ts` - TypeScript interfaces for API data

### stores/
Svelte reactive stores for global state:
- `auth.ts` - Authentication state and methods
- `categories.ts` - Category list with CRUD operations

### components/
Reusable UI components (minimal currently - most UI is in routes)

### assets/
Static assets like images and icons

## Import Usage

```typescript
// API client
import { api } from '$lib/api/client';

// Types
import type { Transaction, Category, Budget } from '$lib/api/types';

// Stores
import { auth } from '$lib/stores/auth';
import { categories } from '$lib/stores/categories';
```

## API Client Pattern

The API client is a singleton class that handles:
- Base URL configuration
- JWT token management (localStorage)
- Request/response handling
- Error parsing

```typescript
// Example usage in a component
const transactions = await api.getTransactions({
  start_date: '2026-01-01',
  end_date: '2026-01-31',
  type: 'expense'
});
```

## Store Pattern

Stores use Svelte's `writable` for reactive state:

```typescript
// In a component
import { auth } from '$lib/stores/auth';

// Subscribe to changes
$: isLoggedIn = $auth.isAuthenticated;

// Call store methods
await auth.login(pin);
await auth.logout();
```

## Best Practices

1. **Type Safety**: All API responses are typed
2. **Error Handling**: API client throws on errors
3. **Token Management**: Automatic Bearer token inclusion
4. **Store Updates**: Methods update store state after API calls
5. **Reactivity**: Use `$` prefix for store subscriptions
