# Routes - CLAUDE.md

> **Location:** `frontend/src/routes/`
> **Parent:** [`frontend/src/`](../CLAUDE.md)
> **Siblings:** None at this level (routes is primary content)

## Purpose

SvelteKit file-based routing. Each directory or `+page.svelte` file defines a route. The `+layout.svelte` provides shared UI (sidebar navigation) across all pages.

---

## Route Map (10 pages)

| Path | File | Purpose |
|------|------|---------|
| `/` | `+page.svelte` | Dashboard - financial overview |
| `/login` | `login/+page.svelte` | PIN setup and authentication |
| `/transactions` | `transactions/+page.svelte` | Transaction CRUD with filtering |
| `/budgets` | `budgets/+page.svelte` | Monthly budget management |
| `/recurring` | `recurring/+page.svelte` | Recurring transaction setup |
| `/goals` | `goals/+page.svelte` | Savings goal tracking |
| `/banking` | `banking/+page.svelte` | Open Banking integration |
| `/reports` | `reports/+page.svelte` | Charts and analytics |
| `/settings` | `settings/+page.svelte` | PIN change, categories, CSV import |
| - | `+layout.svelte` | Root layout with sidebar |

---

## +layout.svelte (Root Layout)

**Purpose:** Shared navigation wrapper for all pages

**Features:**
- Sidebar navigation (220px fixed, dark blue #2c3e50)
- Auth state subscription and route protection
- Redirects to `/login` if not authenticated
- Logout button

**$effect Block:**
```typescript
$effect(() => {
  const unsubscribe = auth.subscribe((state) => {
    if (!state.loading && !state.isAuthenticated && !$page.url.pathname.startsWith('/login')) {
      goto('/login');
    }
  });
  return unsubscribe;
});
```

**Navigation Items:**
Dashboard, Transactions, Budgets, Recurring, Goals, Banking, Reports, Settings

---

## +page.svelte (Dashboard)

**State:** `summary`, `budgetStatus`, `goals`, `loading`

**API Calls:** `getMonthlySummary`, `getBudgetStatus`, `getGoals` (parallel via Promise.all)

**Sections:**
- Summary cards (income, expenses, net)
- Budget status with progress bars
- Savings goals progress

---

## login/+page.svelte

**State:** `pin`, `confirmPin`, `error`, `isSetup`, `loading`

**Modes:**
- **Setup mode:** New PIN creation with confirmation
- **Login mode:** PIN authentication

**Validation:** Minimum 4 characters, confirmation match

---

## transactions/+page.svelte

**State:** `transactions`, `showForm`, `editingId`, `formData`, `filterType`, `filterCategory`

**Features:**
- Filter by type and category
- Modal add/edit form
- Delete with confirmation
- Color-coded amounts (green income, red expense)

**$effect:** Reloads on filter change

---

## budgets/+page.svelte

**State:** `budgets`, `budgetStatus`, `showForm`, `currentMonth`, `formData`

**Features:**
- Month selector
- Progress bars (green < 75%, orange 75-100%, red > 100%)
- Spent/budgeted/remaining display

**$effect:** Reloads on month change

---

## recurring/+page.svelte

**State:** `recurring`, `showForm`, `formData`

**Features:**
- Frequency options (daily/weekly/monthly)
- Active/inactive toggle
- "Process Due" button for manual processing
- Next run date display

---

## goals/+page.svelte

**State:** `goals`, `showForm`, `showContribute`, `formData`, `contributeAmount`

**Features:**
- Grid of goal cards
- Progress percentage and days remaining
- Separate contribution modal

---

## banking/+page.svelte

**State:** `connections`, `pendingTransactions`, `availableBanks`, `syncing`, `showAddBank`, `selectedBank`, `selectedAccount`

**Features:**
- Connect bank accounts
- Sync transactions
- Review pending with category selection
- Import/dismiss individual or bulk

**$effect:** Updates account options when bank selected

---

## reports/+page.svelte

**State:** `trends`, `breakdown`, `currentMonth`, `trendChart`, `breakdownChart`, `trendCanvas`, `breakdownCanvas`

**Chart.js Integration:**
- Bar chart: 6-month income vs expenses
- Doughnut chart: Category expense breakdown
- Charts destroyed and recreated on data change

**$effect:** Reloads on month change

---

## settings/+page.svelte

**State:** `currentPin`, `newPin`, `confirmPin`, `pinError`, `pinSuccess`, `newCategory`, `categoryError`, `csvFile`, `csvPreview`, `importError`, `importSuccess`

**Sections:**
1. Change PIN form
2. Custom categories with color picker
3. Category list (default locked, custom deletable)
4. CSV import with preview

---

## Common Patterns

### Data Loading
```svelte
<script lang="ts">
  import { onMount } from 'svelte';
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
{#if showModal}
  <div class="modal-overlay" onclick={() => showModal = false}>
    <div class="modal" onclick={(e) => e.stopPropagation()}>
      <!-- form content -->
    </div>
  </div>
{/if}
```

### Reactive Filtering
```svelte
$effect(() => {
  if (filterType === 'all') {
    filteredData = data;
  } else {
    filteredData = data.filter(item => item.type === filterType);
  }
});
```

---

## Styling Conventions

| Element | Style |
|---------|-------|
| Cards | White background, 8px radius, subtle shadow |
| Progress bars | 8-10px height, colored fill |
| Modals | Fixed overlay, centered, z-index 100 |
| Amounts | Green (#2ecc71) income, red (#e74c3c) expense |
| Buttons | Primary blue (#3498db), secondary gray, danger red |
