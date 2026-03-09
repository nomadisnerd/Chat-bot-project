# Outreach CRM Backend (MVP Stage 1)

Backend foundation for internship outreach CRM and automation system.

## Tech stack
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic v2

## Project layout
- `app/api` - REST routers and dependencies
- `app/core` - settings and enums
- `app/db` - SQLAlchemy base, types, session
- `app/models` - ORM models
- `app/schemas` - request/response schemas
- `app/crud` - data access logic
- `app/services` - business services (dashboard stats)
- `alembic` - DB migrations

## Quick start
1. Create `.env` from `.env.example`.
2. Start PostgreSQL (Docker compose or local).
3. Run migration: `alembic upgrade head`.
4. Start API: `uvicorn app.main:app --reload`.

Docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

By default, endpoints are mounted without a prefix (for example: `/companies`).
Set `API_V1_STR=/api/v1` in `.env` if you want versioned routes.
