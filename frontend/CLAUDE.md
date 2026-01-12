# Frontend - CLAUDE.md

## Overview

SvelteKit frontend for the Budget App. Provides a modern, responsive UI for personal finance management with transaction tracking, budget monitoring, savings goals, visual reports, and Open Banking integration.

## Tech Stack

- **Framework**: SvelteKit 2.x (full-stack web framework)
- **UI Library**: Svelte 5 (reactive components with runes)
- **Language**: TypeScript (strict mode)
- **Build Tool**: Vite 7.x
- **Charts**: Chart.js 4.x
- **Styling**: CSS (component-scoped)

## Directory Structure

```
frontend/
├── src/
│   ├── lib/
│   │   ├── api/           # API client and TypeScript types
│   │   ├── stores/        # Svelte reactive stores
│   │   ├── components/    # Reusable UI components
│   │   └── assets/        # Static assets
│   ├── routes/            # SvelteKit pages
│   └── app.html           # HTML template
├── static/                # Public static files
├── package.json           # Dependencies and scripts
├── svelte.config.js       # SvelteKit configuration
├── vite.config.ts         # Vite configuration
└── tsconfig.json          # TypeScript configuration
```

## Running the Frontend

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run check
```

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start dev server at http://localhost:5173 |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run check` | Run svelte-check for type errors |
| `npm run check:watch` | Continuous type checking |

## Key Features

- **9 Pages**: Dashboard, Transactions, Budgets, Recurring, Goals, Banking, Reports, Settings, Login
- **Reactive State**: Svelte 5 runes ($state, $effect, $props)
- **API Integration**: Full REST API client with JWT authentication
- **Data Visualization**: Chart.js bar and doughnut charts
- **Form Handling**: Modal-based forms with validation
- **Route Protection**: Client-side auth guards

## Configuration

### Environment
- API Base URL: `http://localhost:8000/api` (hardcoded in client.ts)
- Dev Server Port: 5173 (Vite default)

### TypeScript
- Strict mode enabled
- ES modules with bundler resolution
- Source maps for debugging

## Design System

### Colors
- Primary: #3498db (blue)
- Success/Income: #2ecc71 (green)
- Danger/Expense: #e74c3c (red)
- Warning: #f39c12 (orange)
- Neutral: #ecf0f1, #999, #666

### Layout
- Sidebar navigation (220px fixed)
- Main content area (flex: 1)
- Card-based components
- Modal dialogs for forms
