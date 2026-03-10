# CODEBUDDY.md

This file provides guidance to CodeBuddy Code when working with code in this repository.

## Project Overview

PMS (Portfolio Management System) is a full-stack investment portfolio management application with:
- **Frontend**: Vue 3 + TypeScript + Vite + Pinia + Element Plus + ECharts
- **Backend**: Python + Flask + SQLAlchemy + SQLite + Flask-JWT-Extended

## Development Commands

### Frontend

```bash
npm run dev          # Start dev server on http://localhost:3000
npm run build        # Type-check and build for production
npm run preview      # Preview production build
```

### Frontend Testing

```bash
npm run test         # Run Vitest in watch mode
npm run test:unit    # Run unit tests once
npm run test:coverage # Run tests with coverage

# E2E tests with Playwright
npm run test:e2e     # Run all E2E tests
npm run test:e2e:ui  # Run E2E tests with UI
npm run test:e2e:report # Show test report
```

### Backend

```bash
python app.py        # Start Flask server on http://localhost:5000
pytest               # Run Python unit tests
pytest --cov=app     # Run tests with coverage
```

## Architecture

### Frontend Structure (`src/`)

- **`views/`**: Page components organized by feature (auth, portfolio, asset, performance, market, cash, report)
- **`components/layout/`**: Shared layout components (Layout, Sidebar, TopNav)
- **`store/modules/`**: Pinia stores for state management (user, portfolio)
- **`api/services/`**: API service modules for backend communication
- **`utils/http.ts`**: Axios wrapper with JWT token injection and error handling
- **`types/index.ts`**: TypeScript interfaces for all data models
- **`router/index.ts`**: Vue Router config with auth guards

### Backend Structure (`app/`)

- **`api/`**: Flask-RESTx API namespaces (auth, portfolio, asset, holding, transaction, cash_flow, performance, market, report)
- **`models/`**: SQLAlchemy ORM models
- **`schemas/`**: Marshmallow schemas for request/response validation
- **`services/`**: Business logic layer (separate from API routes)
- **`config/`**: Environment-based configuration (development/testing/production)
- **`utils/database.py`**: Database connection setup

### API Architecture

The backend uses Flask application factory pattern (`create_app()`). API routes are organized by resource:
- `/api/auth` - Authentication endpoints
- `/api/portfolios` - Portfolio CRUD
- `/api/portfolios/<id>/holdings` - Nested holdings under portfolio
- `/api/portfolios/<id>/transactions` - Nested transactions
- `/api/assets` - Asset management
- `/api/market` - Market data
- `/api/reports` - Report generation

Swagger documentation available at `/docs` when backend is running.

### Key Patterns

1. **Frontend-Backend Communication**:
   - All API calls go through `src/utils/http.ts` which auto-injects JWT tokens
   - API services in `src/api/services/` export typed async functions
   - Vite proxy forwards `/api` requests to `http://localhost:5000`

2. **State Management**:
   - Pinia stores use composition API style with `defineStore('name', () => {...})`
   - Token stored in localStorage and managed by user store

3. **Route Protection**:
   - Routes with `meta: { requiresAuth: true }` require valid JWT token
   - Router guard redirects unauthenticated users to `/auth/login`

4. **Backend Layer Separation**:
   - API routes in `app/api/` handle HTTP concerns
   - Business logic in `app/services/`
   - Data validation via schemas in `app/schemas/`

## Data Models

Core entities: User, Portfolio, Asset, Holding, Transaction, CashFlow, MarketData, Report

TypeScript interfaces defined in `src/types/index.ts`

SQLAlchemy models in `app/models/`

## Test Accounts

Default test account: `test123@example.com` / `123456`
