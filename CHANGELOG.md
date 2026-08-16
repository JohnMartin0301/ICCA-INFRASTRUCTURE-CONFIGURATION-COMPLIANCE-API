# Changelog

All notable changes to ICCA are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.2.0] - 2026-08-16

### Added

- PostgreSQL database integration
- SQLAlchemy `Server` model with a database-enforced unique `hostname` constraint
- Database session management via a FastAPI dependency (`get_db`)
- Alembic migration setup and initial `servers` table migration
- Environment-based configuration (`app/core/config.py`, `.env`, `.env.example`)

### Changed

- Replaced the in-memory `servers_db` dictionary with persistent PostgreSQL storage
- `POST`/`PATCH /servers` now return `400` via a caught `IntegrityError` instead of a manual duplicate check

## [0.1.0] - 2026-08-15

### Added

- Initial FastAPI application structure (`app/main.py`, `app/api/`, `app/schemas/`)
- Server resource CRUD endpoints: create, list, get one, update (PATCH), delete
- In-memory server storage (temporary — replaced by PostgreSQL in the next phase)
- Request/response validation via Pydantic models (`ServerCreate`, `ServerUpdate`, `ServerOut`)
- Duplicate hostname prevention on server creation (400 response)
- `404` handling for operations on a nonexistent server
- `/health` endpoint