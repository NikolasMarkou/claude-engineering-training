# Routes - CLAUDE.md

## Overview

SvelteKit file-based routing. Each directory or `+page.svelte` file defines a route. The `+layout.svelte` provides shared UI across all pages.

## Route Structure

```
routes/
├── +layout.svelte       # Root layout (sidebar, auth guard)
├── +page.svelte         # Dashboard (/)
├── login/
│   └── +page.svelte     # Login/Setup (/login)
├── transactions/
│   └── +page.svelte     # Transactions (/transactions)
├── budgets/
│   └── +page.svelte     # Budgets (/budgets)
├── recurring/
│   └── +page.svelte     # Recurring (/recurring)
├── goals/
│   └── +page.svelte     # Goals (/goals)
├── banking/
│   └── +page.svelte     # Banking (/banking)
├── reports/
│   └── +page.svelte     # Reports (/reports)
└── settings/
    └── +page.svelte     # Settings (/settings)
```

## Pages

### +layout.svelte (Root Layout)
- **Purpose**: Shared UI wrapper for all pages
- **Features**:
  - Sidebar navigation (220px fixed width)
  - Auth state subscription and route protection
  - Redirects to `/login` if not authenticated
  - Logout button
- **Styling**: Dark blue sidebar (#2c3e50), light gray content area

### +page.svelte (Dashboard)
- **Route**: `/`
- **Purpose**: Financial overview and quick stats
- **Features**:
  - Monthly summary (income, expenses, net)
  - Budget status cards with progress bars
  - Savings goals progress
  - Parallel data loading with `Promise.all()`

### login/+page.svelte
- **Route**: `/login`
- **Purpose**: PIN authentication
- **Features**:
  - Detects setup vs login state
  - PIN creation with confirmation (min 4 chars)
  - Redirects to dashboard on success
  - Error message display

### transactions/+page.svelte
- **Route**: `/transactions`
- **Purpose**: Transaction CRUD
- **Features**:
  - List all transactions with category badges
  - Filter by type and category
  - Modal form for add/edit
  - Delete confirmation
  - Color-coded amounts (green/red)

### budgets/+page.svelte
- **Route**: `/budgets`
- **Purpose**: Monthly budget management
- **Features**:
  - Month selector
  - Budget status with progress bars
  - Visual warnings (orange 75%, red 100%+)
  - Add/delete budgets via modal

### recurring/+page.svelte
- **Route**: `/recurring`
- **Purpose**: Recurring transaction setup
- **Features**:
  - List recurring transactions
  - Frequency options (daily/weekly/monthly)
  - Active/inactive toggle
  - "Process Due" button
  - Next run date display

### goals/+page.svelte
- **Route**: `/goals`
- **Purpose**: Savings goal tracking
- **Features**:
  - Grid of goal cards
  - Progress percentage and days remaining
  - Contribution modal
  - Create/edit/delete goals

### banking/+page.svelte
- **Route**: `/banking`
- **Purpose**: Open Banking integration
- **Features**:
  - Connected accounts with balances
  - Add bank connection modal
  - Sync button per account
  - Pending transactions review
  - Import/dismiss actions
  - Bulk import all

### reports/+page.svelte
- **Route**: `/reports`
- **Purpose**: Analytics and visualizations
- **Features**:
  - 6-month income vs expenses bar chart
  - Category breakdown doughnut chart
  - Monthly summary table
  - Month selector for breakdown

### settings/+page.svelte
- **Route**: `/settings`
- **Purpose**: Configuration and import
- **Features**:
  - Change PIN form
  - Create custom categories
  - Category list (default locked)
  - CSV import with preview

## Common Patterns

### Page Data Loading
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
  import { api } from '$lib/api/client';

  let data = $state([]);
  let loading = $state(true);

  onMount(async () => {
    data = await api.getData();
    loading = false;
  });
</script>
```

### Modal Forms
```svelte
<script lang="ts">
  let showModal = $state(false);
  let formData = $state({ name: '', amount: 0 });

  async function handleSubmit() {
    await api.createItem(formData);
    showModal = false;
    await loadData();
  }
</script>

{#if showModal}
  <div class="modal-overlay" onclick={() => showModal = false}>
    <div class="modal" onclick={(e) => e.stopPropagation()}>
      <form onsubmit={handleSubmit}>
        <!-- form fields -->
      </form>
    </div>
  </div>
{/if}
```

### Filtering with $effect
```svelte
<script lang="ts">
  let filterType = $state('all');
  let filteredData = $state([]);

  $effect(() => {
    if (filterType === 'all') {
      filteredData = data;
    } else {
      filteredData = data.filter(item => item.type === filterType);
    }
  });
</script>
```

## Styling Conventions

- Component-scoped `<style>` blocks
- CSS variables for colors
- Flexbox/Grid layouts
- Card-based components
- Modal overlays with semi-transparent background
- Progress bars with percentage width
- Color-coded status (green/orange/red)
