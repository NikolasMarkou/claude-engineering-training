# Stores - CLAUDE.md

## Overview

Svelte reactive stores for managing global application state. Uses Svelte's `writable` store primitive for reactive updates across components.

## Files

### auth.ts - Authentication Store

Manages authentication state and provides login/logout methods.

**State:**
```typescript
interface AuthState {
  isAuthenticated: boolean;  // User has valid token
  isSetup: boolean;          // PIN has been configured
  loading: boolean;          // Checking auth status
}
```

**Methods:**

`checkStatus()`
- Called on app initialization
- Checks `/api/auth/status` endpoint
- Sets `isSetup` based on response
- Validates existing token if present
- Updates `isAuthenticated` accordingly

`setup(pin: string)`
- Creates new PIN via `/api/auth/setup`
- Stores returned JWT token
- Sets `isAuthenticated = true`

`login(pin: string)`
- Authenticates via `/api/auth/login`
- Stores returned JWT token
- Sets `isAuthenticated = true`

`logout()`
- Clears token from localStorage
- Sets `isAuthenticated = false`
- Does NOT reset `isSetup`

**Usage:**
```svelte
<script lang="ts">
  import { auth } from '$lib/stores/auth';

  // Subscribe to state changes
  let authState = $state($auth);

  // Or use $ prefix in template
</script>

{#if $auth.loading}
  <p>Loading...</p>
{:else if $auth.isAuthenticated}
  <button onclick={() => auth.logout()}>Logout</button>
{:else}
  <a href="/login">Login</a>
{/if}
```

### categories.ts - Categories Store

Manages the list of transaction categories.

**State:**
```typescript
type CategoriesState = Category[];
```

**Methods:**

`load()`
- Fetches all categories from `/api/categories`
- Updates store with response array
- Called on app initialization and after mutations

`create(data: CategoryCreate)`
- Creates new category via `/api/categories`
- Calls `load()` to refresh list

`delete(id: number)`
- Deletes category via `/api/categories/{id}`
- Calls `load()` to refresh list
- Note: Default categories cannot be deleted

**Usage:**
```svelte
<script lang="ts">
  import { categories } from '$lib/stores/categories';
  import { onMount } from 'svelte';

  onMount(() => {
    categories.load();
  });
</script>

<select>
  {#each $categories as category}
    <option value={category.id}>{category.name}</option>
  {/each}
</select>
```

## Store Pattern

Both stores follow this pattern:

```typescript
import { writable } from 'svelte/store';
import { api } from '$lib/api/client';

// Create writable store with initial state
const { subscribe, set, update } = writable<State>(initialState);

// Export store with methods
export const storeName = {
  subscribe,  // Required for $ reactivity

  async method() {
    // Call API
    const result = await api.endpoint();
    // Update store
    set(result);
    // Or
    update(state => ({ ...state, field: value }));
  }
};
```

## Reactivity

Stores integrate with Svelte's reactivity system:

```svelte
<script>
  import { auth } from '$lib/stores/auth';

  // Method 1: $ prefix (auto-subscription)
  $: isLoggedIn = $auth.isAuthenticated;

  // Method 2: Manual subscription
  let authState;
  const unsubscribe = auth.subscribe(value => {
    authState = value;
  });
  onDestroy(unsubscribe);

  // Method 3: Svelte 5 $state (in +layout.svelte)
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

## Best Practices

1. **Centralized State**: Use stores for data shared across multiple components
2. **API Integration**: Store methods should call API and update state
3. **Loading States**: Track loading status for async operations
4. **Cleanup**: Unsubscribe in `onDestroy` when manually subscribing
5. **Type Safety**: Use TypeScript interfaces for store state
