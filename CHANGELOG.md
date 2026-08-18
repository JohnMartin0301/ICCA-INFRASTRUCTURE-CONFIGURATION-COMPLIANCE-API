# Changelog

All notable changes to ICCA are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.4.0] - 2026-08-18

### Added

- `Finding` model with database-enforced prevention of duplicate open findings (partial unique index on server+check, scoped to `status = 'open'`)
- Automatic finding reconciliation on validation submission: first failure opens a finding, repeated failures update it, a passing result resolves it
- `app/services/finding_service.py` — `reconcile_finding()`, the core duplicate-prevention/auto-resolve logic
- Read-only findings API (`GET /findings`, `GET /findings/{id}`)

### Changed

- `submit_validation_run()` now calls finding reconciliation for every submitted result, as part of the same transaction as the validation run and its results
- Added a `409 Conflict` safety net around validation-run commits, backing the new database constraint

## [0.3.0] - 2026-08-17

### Added

- Configuration check management (`POST/GET /checks`, `GET /checks/{id}`)
- Validation run submission (`POST /servers/{server_id}/validation-runs`)
- `ValidationRun` and `ValidationResult` models, with relationships to `Server` and `Check`
- Pass/fail determination by comparing submitted `actual_value` against a check's `expected_value`
- `app/services/validation_service.py` — first use of a service-layer function for multi-table transaction logic

### Changed

- Extended the database schema with `checks`, `validation_runs`, and `validation_results` tables

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