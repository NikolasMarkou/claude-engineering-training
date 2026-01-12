# Stores - CLAUDE.md

> **Location:** `frontend/src/lib/stores/`
> **Parent:** [`frontend/src/lib/`](../CLAUDE.md)
> **Siblings:** [`api/`](../api/CLAUDE.md)

## Purpose

Svelte reactive stores for managing global application state. Uses Svelte's `writable` store primitive for reactive updates across components.

---

## Files

| File | Store | Purpose |
|------|-------|---------|
| `auth.ts` | `auth` | Authentication state and methods |
| `categories.ts` | `categories` | Category list with CRUD operations |

---

## auth.ts - Authentication Store

### State Interface

```typescript
interface AuthState {
  isAuthenticated: boolean;  // Has valid JWT token
  isSetup: boolean;          // PIN has been configured
  loading: boolean;          // Checking auth status
}

// Initial state
{
  isAuthenticated: false,
  isSetup: false,
  loading: true
}
```

### Methods

#### `checkStatus(): Promise<void>`
Called on app initialization to verify authentication.

```typescript
// Logic:
1. Set loading = true
2. Call api.getAuthStatus()
3. Check api.isAuthenticated() for token validity
4. Update isAuthenticated and isSetup
5. Set loading = false
```

#### `setup(pin: string): Promise<void>`
Creates initial PIN for new users.

```typescript
// Logic:
1. Call api.setupPin(pin)
2. Token automatically stored by API client
3. Set isAuthenticated = true, isSetup = true
```

#### `login(pin: string): Promise<void>`
Authenticates with existing PIN.

```typescript
// Logic:
1. Call api.login(pin)
2. Token automatically stored by API client
3. Set isAuthenticated = true
```

#### `logout(): void`
Clears authentication state.

```typescript
// Logic:
1. Call api.clearToken()
2. Set isAuthenticated = false
3. Keep isSetup = true (PIN still exists)
```

### Usage

```svelte
<script lang="ts">
  import { auth } from '$lib/stores/auth';

  // Auto-subscription with $ prefix
</script>

{#if $auth.loading}
  <p>Loading...</p>
{:else if $auth.isAuthenticated}
  <button onclick={() => auth.logout()}>Logout</button>
{:else}
  <a href="/login">Login</a>
{/if}
```

---

## categories.ts - Categories Store

### State

```typescript
type CategoriesState = Category[];

// Initial state: empty array
[]
```

### Methods

#### `load(): Promise<void>`
Fetches all categories from API.

```typescript
// Logic:
1. Call api.getCategories()
2. Set store to returned array
```

#### `create(data: Partial<Category>): Promise<Category>`
Creates a new custom category.

```typescript
// Logic:
1. Call api.createCategory(data)
2. Call this.load() to refresh
3. Return created category

// Required fields:
- name: string
- type: 'income' | 'expense'
// Optional:
- icon: string
- color: string
```

#### `delete(id: number): Promise<void>`
Deletes a custom category.

```typescript
// Logic:
1. Call api.deleteCategory(id)
2. Call this.load() to refresh

// Note: Default categories (is_default=true) cannot be deleted
```

### Usage

```svelte
<script lang="ts">
  import { categories } from '$lib/stores/categories';
  import { onMount } from 'svelte';

  onMount(() => categories.load());
</script>

<select>
  {#each $categories as category}
    <option value={category.id}>{category.name}</option>
  {/each}
</select>
```

---

## Store Pattern

Both stores follow this implementation pattern:

```typescript
import { writable } from 'svelte/store';
import { api } from '$lib/api/client';

function createStore() {
  const { subscribe, set, update } = writable<State>(initialState);

  return {
    subscribe,  // Required for $ reactivity

    async method() {
      const result = await api.endpoint();
      set(result);
      // or
      update(state => ({ ...state, field: value }));
    }
  };
}

export const storeName = createStore();
```

---

## Reactivity Integration

### Method 1: Auto-subscription ($ prefix)
```svelte
{#if $auth.isAuthenticated}
  <p>Logged in</p>
{/if}
```

### Method 2: Reactive statement
```svelte
<script>
  $: isLoggedIn = $auth.isAuthenticated;
</script>
```

### Method 3: $effect (Svelte 5)
```svelte
<script>
  $effect(() => {
    const unsubscribe = auth.subscribe((state) => {
      if (!state.loading && !state.isAuthenticated) {
        goto('/login');
      }
    });
    return unsubscribe;
  });
</script>
```

---

## Store Dependencies

```
auth.ts
  └── api/client.ts (api.getAuthStatus, api.setupPin, api.login, api.clearToken)

categories.ts
  └── api/client.ts (api.getCategories, api.createCategory, api.deleteCategory)
```

---

## Used By

| Store | Components |
|-------|------------|
| `auth` | `+layout.svelte`, `login/+page.svelte` |
| `categories` | `transactions/+page.svelte`, `budgets/+page.svelte`, `recurring/+page.svelte`, `banking/+page.svelte`, `settings/+page.svelte` |
