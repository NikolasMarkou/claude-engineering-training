# Frontend Source - CLAUDE.md

> **Location:** `frontend/src/`
> **Parent:** [`frontend/`](../CLAUDE.md)
> **Children:** [`lib/`](lib/CLAUDE.md), [`routes/`](routes/CLAUDE.md)

## Purpose

Main source directory for the SvelteKit application. Contains all application code including library modules, routes/pages, and the HTML template.

---

## Directory Structure

```
src/
├── lib/                    # Shared library code ($lib alias)
│   ├── api/               # REST API client & types
│   │   ├── client.ts      # API methods (38 total)
│   │   └── types.ts       # TypeScript interfaces
│   ├── stores/            # Svelte reactive stores
│   │   ├── auth.ts        # Authentication state
│   │   └── categories.ts  # Category list
│   ├── components/        # Reusable UI (empty)
│   └── assets/            # Static assets
├── routes/                # SvelteKit pages (10 pages)
│   ├── +layout.svelte     # Root layout (sidebar)
│   ├── +page.svelte       # Dashboard (/)
│   ├── login/             # Authentication
│   ├── transactions/      # Transaction CRUD
│   ├── budgets/           # Monthly budgets
│   ├── recurring/         # Recurring transactions
│   ├── goals/             # Savings goals
│   ├── banking/           # Open Banking
│   ├── reports/           # Analytics
│   └── settings/          # Configuration
└── app.html               # HTML shell template
```

---

## Key Files

### app.html
HTML template with SvelteKit placeholders:
```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    %sveltekit.head%
  </head>
  <body>
    <div>%sveltekit.body%</div>
  </body>
</html>
```

### lib/
Shared code accessible via `$lib` alias:
- API client with 38 endpoint methods
- TypeScript types for all data models
- Authentication and categories stores

### routes/
File-based routing:
- Each `+page.svelte` defines a page
- `+layout.svelte` provides shared UI
- Nested directories create nested routes

---

## Import Patterns

### $lib Alias
```typescript
import { api } from '$lib/api/client';
import { auth } from '$lib/stores/auth';
import type { Transaction } from '$lib/api/types';
```

### Inter-route Navigation
```typescript
import { goto } from '$app/navigation';
import { page } from '$app/stores';

// Navigate programmatically
goto('/login');

// Access current route
$page.url.pathname
```

---

## Svelte 5 Features Used

### Reactive State ($state)
```svelte
<script lang="ts">
  let transactions = $state<Transaction[]>([]);
  let loading = $state(true);
</script>
```

### Derived Values ($derived)
```svelte
<script lang="ts">
  let filtered = $derived(
    transactions.filter(t => t.type === filterType)
  );
</script>
```

### Side Effects ($effect)
```svelte
<script lang="ts">
  $effect(() => {
    loadData();
  });
</script>
```

### Props ($props)
```svelte
<script lang="ts">
  let { children } = $props();
</script>
```

---

## Application Flow

```
app.html (shell)
    ↓
+layout.svelte (auth check, sidebar)
    ↓
+page.svelte (route content)
    ↓
$lib/api (data fetching)
    ↓
$lib/stores (state management)
    ↓
Reactive UI updates
```

---

## Authentication Flow

1. **App loads** → `+layout.svelte` calls `auth.checkStatus()`
2. **Not authenticated** → Redirect to `/login`
3. **Login page** → User enters PIN
4. **Auth success** → Token stored, redirect to dashboard
5. **Authenticated requests** → JWT in Authorization header
6. **Logout** → Clear token, redirect to `/login`

---

## Page Summary

| Page | Features | Main Components |
|------|----------|-----------------|
| Dashboard | Summary cards, budget/goal progress | Cards, progress bars |
| Transactions | CRUD, filtering | List, modal form |
| Budgets | Month selector, progress tracking | Grid, progress bars |
| Recurring | Frequency options, process button | List, toggle, form |
| Goals | Contributions, progress | Grid, contribution modal |
| Banking | Bank sync, pending review | Account cards, pending list |
| Reports | Chart.js graphs | Bar chart, doughnut chart |
| Settings | PIN change, categories, CSV | Forms, file upload |
