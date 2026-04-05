# Finance Dashboard API
<p align="center">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/RESTful-API-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white">
  <img src="https://img.shields.io/badge/SQLModel-ORM-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white">
</p>

A backend system for finance data processing with role-based access control, built as a clean and well-reasoned assessment submission.

> The goal of this implementation was to balance simplicity with real-world backend practices rather than over-engineering the solution.


## Tech Stack

| Layer        | Tool                        |
|--------------|-----------------------------|
| Framework    | FastAPI                     |
| ORM          | SQLModel (SQLAlchemy core)  |
| Database     | SQLite                      |
| Auth         | JWT (python-jose + bcrypt)  |
| Validation   | Pydantic v2                 |
| Rate Limiting| slowapi                     |
| API Docs     | Swagger (auto-generated)    |


## Project Structure

```
finance-backend/                    # Root project directory
├── app/                            # Core backend application (business logic + API)
│   ├── core/                       # Cross-cutting concerns (auth, RBAC, exceptions, rate limiting)
│   │   ├── auth.py
│   │   ├── rbac.py
│   │   ├── exception.py
│   │   ├── rate_limit.py
│   │   └── bootstrap.py
│   │
│   ├── models/                     # Database models (SQLModel ORM classes)
│   │   ├── user.py
│   │   └── record.py
│   │
│   ├── routes/                     # API endpoints (request/response layer)
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── records.py
│   │   └── dashboard.py
│   │
│   ├── schemas/                    # Pydantic schemas (validation + serialization)
│   │   ├── user.py
│   │   ├── record.py
│   │   └── dashboard.py
│   │
│   ├── services/                   # Business logic + DB queries (no HTTP logic)
│   │   ├── user_service.py
│   │   ├── record_service.py
│   │   └── dashboard_service.py
│   │
│   ├── __init__.py
│   ├── config.py                   # Environment config (loads from .env)
│   ├── db.py                       # Database engine + session dependency
│   └── main.py                     # FastAPI app entrypoint + router registration
│
├── bruno/                          # API testing collections (manual testing using Bruno)
│   ├── auth/                       # Auth flow tests (register, login, token usage)
│   ├── users/                      # Admin user management endpoints
│   ├── records/                    # CRUD + filters for financial records
│   ├── dashboard/                  # Analytics endpoints (summary, trends, breakdown)
│   └── environments/               # Environment configs (local/dev variables)
│
├── seed.py                         # Script to populate DB with sample users and records
├── requirements.txt                # Python dependencies (pinned versions)
├── README.md                       # Project documentation and setup guide
├── .env.example                    # Sample environment variables
├── .gitignore                      # Files/folders ignored by Git
└── finance.db                      # SQLite database file (ignored in Git)
```


## Architecture Decisions

**1. SQLite** — Zero configuration. Schema and raw queries are fully visible and inspectable. Swap `DATABASE_URL` to PostgreSQL for production with no code changes needed.

**2. SQLModel** — Combines SQLAlchemy table definitions and Pydantic validation in a single class. Eliminates duplicate model definitions.

**3. Separation of concerns** — Routes handle HTTP request/response only. Services contain all business logic and DB queries. Models define schema. No business logic leaks into route handlers.

**4. RBAC via dependency injection** — `RoleChecker` is a callable class injected as a FastAPI dependency. No decorators, no scattered if-checks — clean, reusable, and testable.

**5. SQL-level aggregation** — Dashboard summary and category breakdown use `func.sum`, `func.count`, and `GROUP BY` at the database level instead of Python loops. Signals database awareness and scales better.

**6. Soft delete** — Financial records are marked `is_deleted=True` instead of being permanently removed. Preserves audit history and allows recovery — standard practice in finance systems.

**7. Currency field** — Each record carries a `currency` code (default: INR). Small addition that makes the data model realistic for a finance system.

**8. Simple JWT** — Single access token with configurable expiry. No refresh token complexity — sufficient for assessment scope.

**9. Timestamps** — `updated_at` is manually set in service functions during updates and soft deletes rather than using ORM-level event hooks. Keeps logic explicit and visible during code review. In production, SQLAlchemy `@event.listens_for` or database-level triggers would automate this.

**10. Rate limiting** — Endpoint-specific rate limits implemented with slowapi. In-memory storage used for assessment; would be swapped to Redis in production.


## Role Permissions Matrix

| Action                        | Viewer | Analyst | Admin |
|-------------------------------|--------|---------|-------|
| View own profile              | ✅     | ✅      | ✅    |
| View financial records        | ✅     | ✅      | ✅    |
| View dashboard summary        | ✅     | ✅      | ✅    |
| View recent activity          | ✅     | ✅      | ✅    |
| View category breakdown       | ❌     | ✅      | ✅    |
| View monthly trends           | ❌     | ✅      | ✅    |
| Create / update / delete records | ❌  | ❌      | ✅    |
| Manage users (role / status)  | ❌     | ❌      | ✅    |



## Setup & Run

### Prerequisites
- Python 3.10+

### Steps

```bash
# 1. Clone and enter project
git clone https://github.com/Average-Chief/Finance_Dashboard.git
cd Finance_Dashboard

# 2. Create and activate virtual environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment file
copy .env.example .env

# 5. Seed database with test data
python seed.py

# 6. Start server
uvicorn app.main:app --reload
```

Once running, interactive API docs are available at:
**`http://localhost:8000/docs`**


## Environment Variables

```env
# .env.example
secret_key=super-secret-key
database_url=sqlite:///your.db
access_token_expires_in=30
```


## Test Credentials

After running `seed.py`, the following accounts are available:

| Role    | Email                   | Password    |
|---------|-------------------------|-------------|
| Admin   | admin@firm.com       | admin123    |
| Analyst | analyst@firm.com     | analyst123  |
| Viewer  | viewer@firm.com      | viewer123   |

If no users exist (ex: on first deploy), a default admin user is automatically created:

| Role  | Email              | Password  |
|-------|--------------------|-----------|
| Admin | admin@firm.com  | admin123  |

## Live API

Deployed API (Render):
https://finance-dashboard-z76y.onrender.com

For API Docs:
https://finance-dashboard-z76y.onrender.com/docs

Note: The service runs on Render free tier, so the first request may take a few seconds due to cold start.

## API Reference

### Authentication

| Method | Endpoint         | Description              | Access |
|--------|------------------|--------------------------|--------|
| POST   | `/auth/register` | Register new user        | Public |
| POST   | `/auth/login`    | Login → JWT token        | Public |
| GET    | `/auth/me`       | Current user profile     | Any    |

### User Management

| Method | Endpoint               | Description           | Access |
|--------|------------------------|-----------------------|--------|
| GET    | `/users/`              | List all users        | Admin  |
| GET    | `/users/{id}`          | Get user by ID        | Admin  |
| PATCH  | `/users/{id}/role`     | Change user role      | Admin  |
| PATCH  | `/users/{id}/status`   | Activate / deactivate | Admin  |

### Financial Records

| Method | Endpoint         | Description                      | Access |
|--------|------------------|----------------------------------|--------|
| POST   | `/records/`      | Create record                    | Admin  |
| GET    | `/records/`      | List with filters + pagination   | All    |
| GET    | `/records/{id}`  | Get single record                | All    |
| PUT    | `/records/{id}`  | Update record                    | Admin  |
| DELETE | `/records/{id}`  | Soft delete record               | Admin  |

**Query filters on `GET /records/`:**

| Param        | Type   | Description              |
|--------------|--------|--------------------------|
| `type`       | string | `income` or `expense`    |
| `category`   | string | Category name            |
| `start_date` | date   | From date (YYYY-MM-DD)   |
| `end_date`   | date   | To date (YYYY-MM-DD)     |
| `skip`       | int    | Pagination offset        |
| `limit`      | int    | Records per page (1–100) |

### Dashboard & Analytics

| Method | Endpoint                      | Description                      | Access          |
|--------|-------------------------------|----------------------------------|-----------------|
| GET    | `/dashboard/summary`          | Total income / expense / balance | All             |
| GET    | `/dashboard/category-breakdown` | Totals by category + type      | Analyst + Admin |
| GET    | `/dashboard/trends`           | Monthly income vs expense        | Analyst + Admin |
| GET    | `/dashboard/recent`           | Last N transactions              | All             |

## API Testing

All endpoints have been manually tested using Bruno collections.

The requests cover:
- Authentication flows (register, login, token usage)
- Role-based access control (viewer, analyst, admin)
- CRUD operations on financial records
- Filtering and pagination
- Dashboard endpoints

The Bruno collection is available in the `/bruno` folder for reproducibility.

Note: Automated testing was not included as it was outside the scope of the assignment, but the current structure allows easy integration of pytest-based tests.

## Rate Limits

| Scope              | Limit       | Reason                               |
|--------------------|-------------|--------------------------------------|
| Auth endpoints     | 5 / minute  | Prevent brute-force login attempts   |
| Standard endpoints | 60 / minute | Normal usage ceiling                 |
| Dashboard endpoints| 30 / minute | Aggregation queries are heavier      |
| Admin write operations | 20 / minute | Controlled mutation rate        |



## Assumptions

1. **Default role is viewer** — new users register as viewers. Only an admin can promote roles.
2. **Records are global** — all authorized users see the same set of records. Not scoped per user.
3. **Category is free-text** — no predefined list. Indexed for query performance.
4. **Soft delete is final via API** — `DELETE` marks `is_deleted=True`. No restore endpoint is exposed (recoverable at DB level by an admin).
5. **Currency defaults to INR** — configurable per record. No cross-currency conversion logic.
6. **Single access token** — 30-minute expiry, configurable via `.env`. No refresh token flow.
7. **No email verification** — registration is immediate. Suitable for internal or assessment use.
8. **Trend data is calendar-month grouped** — monthly trends aggregate by `YYYY-MM`. Weekly trends were not implemented.


## Tradeoffs Considered

- **SQLite over PostgreSQL** — simpler setup for assessment, trivially swappable via `DATABASE_URL`.
- **No refresh tokens** — keeps auth logic simple and readable. A production system would add them.
- **Manual `updated_at`** — explicit over magical. ORM event hooks would be cleaner in production.
- **In-memory rate limiting** — resets on server restart. Redis or Valky would persist limits across instances.
- **No soft-delete restore endpoint** — intentional scope reduction. The data is safe at DB level.