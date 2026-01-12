# Frontend Source - CLAUDE.md

## Overview

Main source directory containing all application code: library modules, routes/pages, and the HTML template.

## Structure

```
src/
├── lib/                   # Shared library code
│   ├── api/              # API client and types
│   ├── stores/           # Reactive state stores
│   ├── components/       # Reusable components
│   └── assets/           # Static assets
├── routes/               # SvelteKit pages
│   ├── +layout.svelte    # Root layout
│   ├── +page.svelte      # Dashboard (/)
│   ├── login/            # Authentication
│   ├── transactions/     # Transaction management
│   ├── budgets/          # Budget tracking
│   ├── recurring/        # Recurring transactions
│   ├── goals/            # Savings goals
│   ├── banking/          # Open Banking
│   ├── reports/          # Analytics
│   └── settings/         # Settings & import
└── app.html              # HTML shell template
```

## Import Aliases

SvelteKit provides the `$lib` alias for imports from the `lib/` directory:

```typescript
// Instead of: import { api } from '../../../lib/api/client'
import { api } from '$lib/api/client';
import { auth } from '$lib/stores/auth';
import type { Transaction } from '$lib/api/types';
```

## Key Files

### app.html
HTML template with placeholders:
- `%sveltekit.head%` - Injected head content
- `%sveltekit.body%` - Rendered page content

### +layout.svelte
Root layout component:
- Sidebar navigation with 8 links
- Auth state subscription
- Route protection (redirects to /login)
- Logout functionality

### +page.svelte (Dashboard)
Home page showing:
- Monthly summary (income, expenses, net)
- Budget status with progress bars
- Savings goals progress

## Svelte 5 Runes

The app uses Svelte 5's new runes syntax:

```svelte
<script lang="ts">
  // Reactive state
  let count = $state(0);

  // Derived values
  let doubled = $derived(count * 2);

  // Side effects
  $effect(() => {
    console.log('Count changed:', count);
  });

  // Props
  let { name } = $props<{ name: string }>();
</script>
```

## Data Flow

```
User Action
    → Event Handler
    → API Client Call
    → Backend Response
    → State Update ($state)
    → Reactive UI Update
```

## Authentication Flow

1. App loads → `auth.checkStatus()` called
2. If not authenticated → redirect to `/login`
3. User enters PIN → `auth.login(pin)` or `auth.setup(pin)`
4. Token stored in localStorage
5. Subsequent API calls include `Authorization: Bearer {token}`
6. Logout clears token and redirects to `/login`
