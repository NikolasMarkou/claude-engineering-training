<p align="center">
  <img src="https://img.shields.io/badge/Budget-App-3498db?style=for-the-badge&logo=cashapp&logoColor=white" alt="Budget App" height="60"/>
</p>

<h1 align="center">Budget App</h1>

<p align="center">
  <strong>Take control of your finances with smart budgeting</strong>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#api-documentation">API Docs</a> •
  <a href="#contributing">Contributing</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Svelte-5-FF3E00?style=flat-square&logo=svelte&logoColor=white" alt="Svelte 5"/>
  <img src="https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License MIT"/>
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square" alt="PRs Welcome"/>
</p>

---

## Overview

**Budget App** is a modern, full-stack personal finance management application designed to help you track expenses, manage budgets, and achieve your savings goals. Built with a clean architecture and intuitive interface, it provides everything you need to take control of your financial life.

Whether you're tracking daily expenses, setting monthly budgets, or saving for a big purchase, Budget App gives you the insights and tools to make smarter financial decisions.

---

## Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Transaction Tracking** | Record income and expenses with categories, descriptions, and dates. Filter by type, category, or date range. |
| **Monthly Budgets** | Set spending limits per category with visual progress bars. Get warnings at 75% and alerts when over budget. |
| **Recurring Transactions** | Automate regular income/expenses (daily, weekly, monthly). Process due transactions with one click. |
| **Savings Goals** | Create goals with target amounts and deadlines. Track progress and add contributions over time. |
| **Visual Reports** | Interactive charts showing income vs expenses trends (6 months) and expense breakdown by category. |
| **CSV Import** | Bulk import transactions from CSV files with preview and validation before confirmation. |
| **PIN Authentication** | Simple, secure single-user authentication with bcrypt hashing and JWT tokens. |

### Open Banking Integration

Connect mock bank accounts and import transactions automatically:

- **Multi-Bank Support** - Chase, Bank of America, Wells Fargo, Capital One (mock)
- **Account Types** - Checking, Savings, Credit Cards
- **Auto-Categorization** - Smart merchant-to-category mapping
- **Review Workflow** - Review and approve imported transactions before adding to ledger
- **Balance Tracking** - Real-time account balance display

> **Note**: The Open Banking feature uses mock data for demonstration. The architecture is designed to easily swap in real providers (Plaid, TrueLayer, etc.).

---

## Tech Stack

### Backend

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic"/>
</p>

- **FastAPI** - High-performance async web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight, file-based database
- **Pydantic** - Data validation and serialization
- **JWT + bcrypt** - Secure authentication

### Frontend

<p>
  <img src="https://img.shields.io/badge/SvelteKit-FF3E00?style=for-the-badge&logo=svelte&logoColor=white" alt="SvelteKit"/>
  <img src="https://img.shields.io/badge/Svelte_5-FF3E00?style=for-the-badge&logo=svelte&logoColor=white" alt="Svelte 5"/>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript"/>
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" alt="Vite"/>
</p>

- **SvelteKit** - Full-stack web framework
- **Svelte 5** - Reactive UI with runes syntax
- **TypeScript** - Type-safe development
- **Chart.js** - Interactive data visualizations
- **Vite** - Lightning-fast build tool

---

## Quick Start

### Prerequisites

- **Python** 3.10 or higher
- **Node.js** 18 or higher
- **npm** (comes with Node.js)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/NikolasMarkou/claude-engineering-training.git
cd claude-engineering-training
```

**2. Set up the backend**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Set up the frontend**

```bash
cd ../frontend
npm install
```

### Running the Application

**Terminal 1 - Start the backend:**

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Start the frontend:**

```bash
cd frontend
npm run dev
```

**Access the application:**

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Documentation** | http://localhost:8000/docs |

### First-Time Setup

1. Open http://localhost:5173 in your browser
2. Create a PIN (minimum 4 characters) on first visit
3. Start adding transactions and setting up budgets!

---

## Project Structure

```
claude-engineering-training/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # App configuration
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # Database models
│   │   │   ├── user.py          # User settings
│   │   │   ├── category.py      # Transaction categories
│   │   │   ├── transaction.py   # Transactions
│   │   │   ├── budget.py        # Monthly budgets
│   │   │   ├── recurring.py     # Recurring transactions
│   │   │   ├── goal.py          # Savings goals
│   │   │   └── bank.py          # Bank connections
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── routers/             # API endpoints
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── transactions.py  # Transaction CRUD
│   │   │   ├── categories.py    # Category management
│   │   │   ├── budgets.py       # Budget tracking
│   │   │   ├── recurring.py     # Recurring transactions
│   │   │   ├── goals.py         # Savings goals
│   │   │   ├── reports.py       # Analytics
│   │   │   ├── import_export.py # CSV import
│   │   │   └── banking.py       # Open Banking
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   └── budget.db                # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── api/             # API client & types
│   │   │   └── stores/          # Svelte stores
│   │   └── routes/              # SvelteKit pages
│   │       ├── +layout.svelte   # Main layout
│   │       ├── +page.svelte     # Dashboard
│   │       ├── login/           # Authentication
│   │       ├── transactions/    # Transaction management
│   │       ├── budgets/         # Budget management
│   │       ├── recurring/       # Recurring transactions
│   │       ├── goals/           # Savings goals
│   │       ├── banking/         # Open Banking
│   │       ├── reports/         # Analytics
│   │       └── settings/        # Settings & import
│   └── package.json
├── CLAUDE.md                    # Development guide
├── CHANGELOG.md                 # Version history
└── README.md                    # This file
```

---

## API Documentation

The API is fully documented with interactive Swagger UI at **http://localhost:8000/docs**.

### Endpoint Categories

| Category | Base Path | Description |
|----------|-----------|-------------|
| **Auth** | `/api/auth` | PIN setup, login, and management |
| **Transactions** | `/api/transactions` | CRUD operations with filtering |
| **Categories** | `/api/categories` | Manage transaction categories |
| **Budgets** | `/api/budgets` | Monthly budget management |
| **Recurring** | `/api/recurring` | Recurring transaction setup |
| **Goals** | `/api/goals` | Savings goals with contributions |
| **Reports** | `/api/reports` | Analytics and summaries |
| **Import** | `/api/import` | CSV import with preview |
| **Banking** | `/api/banking` | Open Banking integration |

### Example Request

```bash
# Get all transactions for January 2026
curl -X GET "http://localhost:8000/api/transactions?start_date=2026-01-01&end_date=2026-01-31" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Security (REQUIRED for production)
SECRET_KEY=your-super-secret-key-change-this

# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///./budget.db

# JWT Settings (optional)
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 1 week

# App Settings (optional)
DEFAULT_CURRENCY=USD
```

### Default Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `SECRET_KEY` | `change-this-in-production` | JWT signing key |
| `DATABASE_URL` | `sqlite:///./budget.db` | Database connection |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` | Token expiration (7 days) |
| `DEFAULT_CURRENCY` | `USD` | Default currency |

> **Security Note**: Always change the `SECRET_KEY` in production environments!

---

## Contributing

Contributions are welcome! Here's how you can help:

### Getting Started

1. **Fork** the repository
2. **Clone** your fork locally
3. **Create a branch** for your feature: `git checkout -b feature/amazing-feature`
4. **Make your changes** and test thoroughly
5. **Commit** with clear messages: `git commit -m "Add amazing feature"`
6. **Push** to your branch: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow existing code style and patterns
- Write meaningful commit messages
- Add tests for new features when applicable
- Update documentation for API changes
- Keep PRs focused on a single feature/fix

### Areas for Contribution

- Bug fixes and issue resolution
- New features and enhancements
- Documentation improvements
- Test coverage expansion
- Performance optimizations
- UI/UX improvements

---

## Roadmap

### Planned Features

- [ ] Multi-currency support
- [ ] Data export (CSV, PDF reports)
- [ ] Real Open Banking integration (Plaid/TrueLayer)
- [ ] Mobile-responsive design improvements
- [ ] Dark mode theme
- [ ] Budget templates
- [ ] Transaction search
- [ ] Category icons customization
- [ ] Spending insights and recommendations

### Known Limitations

- Single-user design (no multi-user/household support yet)
- Backend authentication guards not enforced (development mode)
- Open Banking uses mock data only
- No automated backup system

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Acknowledgments

Built with these amazing technologies:

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SvelteKit](https://kit.svelte.dev/) - Full-stack web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- [Chart.js](https://www.chartjs.org/) - JavaScript charting library
- [Pydantic](https://docs.pydantic.dev/) - Data validation library

---

<p align="center">
  <strong>Made with care for better financial health</strong>
</p>

<p align="center">
  <a href="#budget-app">Back to top</a>
</p>
