# Frontend - CLAUDE.md

> **Location:** `frontend/`
> **Parent:** [Project Root](../CLAUDE.md)
> **Children:** [`src/`](src/CLAUDE.md)
> **Siblings:** [`backend/`](../backend/CLAUDE.md)

## Purpose

SvelteKit frontend for the Budget App. Provides a modern, reactive UI for personal finance management with transaction tracking, budget monitoring, savings goals, visual reports, and Open Banking integration.

---

## Directory Structure

```
frontend/
├── src/
│   ├── lib/                # Shared library ($lib)
│   │   ├── api/           # REST client & types
│   │   └── stores/        # Svelte stores
│   └── routes/            # SvelteKit pages (10)
├── static/                # Public static files
├── package.json           # Dependencies
├── svelte.config.js       # SvelteKit config
├── vite.config.ts         # Vite config
└── tsconfig.json          # TypeScript config
```

---

## Tech Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Framework | SvelteKit | 2.x |
| UI Library | Svelte | 5.x |
| Language | TypeScript | 5.x |
| Build Tool | Vite | 7.x |
| Charts | Chart.js | 4.x |

---

## Quick Start

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Open browser
open http://localhost:5173
```

---

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (port 5173) |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run check` | TypeScript type checking |
| `npm run check:watch` | Continuous type checking |

---

## Pages (10)

| Route | Page | Features |
|-------|------|----------|
| `/` | Dashboard | Summary cards, budget status, goal progress |
| `/login` | Login | PIN setup/authentication |
| `/transactions` | Transactions | CRUD, filtering, categories |
| `/budgets` | Budgets | Monthly limits, progress bars |
| `/recurring` | Recurring | Scheduled transactions |
| `/goals` | Goals | Savings tracking, contributions |
| `/banking` | Banking | Bank connections, pending imports |
| `/reports` | Reports | Charts, analytics |
| `/settings` | Settings | PIN, categories, CSV import |

---

## Key Components

### Layout (`+layout.svelte`)
- Sidebar navigation (220px fixed)
- Authentication guard
- Logout functionality

### API Client (`$lib/api/client.ts`)
- 38 endpoint methods
- JWT token management
- Automatic Authorization header

### Stores (`$lib/stores/`)
- `auth` - Authentication state
- `categories` - Category list

---

## Svelte 5 Features

```svelte
<script lang="ts">
  // Reactive state
  let data = $state([]);

  // Derived values
  let filtered = $derived(data.filter(x => x.active));

  // Side effects
  $effect(() => {
    fetchData();
  });

  // Props
  let { value } = $props();
</script>
```

---

## Styling

### Design System

| Color | Usage | Hex |
|-------|-------|-----|
| Primary | Buttons, links | `#3498db` |
| Success | Income, positive | `#2ecc71` |
| Danger | Expense, negative | `#e74c3c` |
| Warning | Budget warnings | `#f39c12` |
| Sidebar | Navigation bg | `#2c3e50` |

### Common Patterns
- Cards: White background, 8px radius, subtle shadow
- Progress bars: 8-10px height, colored fill
- Modals: Fixed overlay, centered, z-index 100
- Forms: Grid layouts, full-width inputs

---

## API Integration

```typescript
import { api } from '$lib/api/client';

// In onMount or event handler
const transactions = await api.getTransactions({
  start_date: '2026-01-01',
  type: 'expense'
});

await api.createTransaction({
  amount: 50,
  type: 'expense',
  category_id: 1,
  date: '2026-01-12'
});
```

---

## Configuration

### TypeScript (`tsconfig.json`)
- Strict mode enabled
- ES modules
- Source maps

### Svelte (`svelte.config.js`)
- `vitePreprocess()` for preprocessing
- `@sveltejs/adapter-auto` for deployment

### Vite (`vite.config.ts`)
- SvelteKit plugin
- Default port 5173

---

## Chart.js Integration

Used in Reports page:

```typescript
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// Bar chart: Income vs Expenses (6 months)
// Doughnut chart: Category breakdown
```

---

## Related Documentation

- [`src/`](src/CLAUDE.md) - Source directory overview
- [`src/lib/`](src/lib/CLAUDE.md) - Shared library code
- [`src/lib/api/`](src/lib/api/CLAUDE.md) - API client
- [`src/lib/stores/`](src/lib/stores/CLAUDE.md) - Reactive stores
- [`src/routes/`](src/routes/CLAUDE.md) - Pages and routing
