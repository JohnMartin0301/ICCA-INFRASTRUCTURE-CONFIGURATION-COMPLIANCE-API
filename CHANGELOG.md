# Changelog

All notable changes to ICCA are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.0] - 2026-08-15

### Added

- Initial FastAPI application structure (`app/main.py`, `app/api/`, `app/schemas/`)
- Server resource CRUD endpoints: create, list, get one, update (PATCH), delete
- In-memory server storage (temporary — replaced by PostgreSQL in the next phase)
- Request/response validation via Pydantic models (`ServerCreate`, `ServerUpdate`, `ServerOut`)
- Duplicate hostname prevention on server creation (400 response)
- `404` handling for operations on a nonexistent server
- `/health` endpoint