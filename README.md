# ICCA — Infrastructure Configuration & Compliance API

## Overview
ICCA is a backend API for tracking infrastructure configuration and compliance. It doesn't connect to servers or run commands against them — an external process submits validation results, and ICCA takes it from there: storing results, tracking failures as findings, and keeping track of remediation work until they're resolved.

## Key Features
- Server inventory (CRUD)
- Configuration check definitions
- Validation run submission with automatic pass/fail evaluation
- Automatic finding creation, with duplicate prevention
- Automatic finding resolution when a check passes again
- Remediation tracking with a controlled status flow
- JWT authentication with role-based access (viewer / engineer / admin)
- Pagination and filtering on list endpoints

## Architecture
Modular monolith:
```
app/
├── api/ # routes
├── core/ # config and security
├── db/ # database setup
├── models/ # SQLAlchemy models
├── schemas/ # Pydantic schemas
├── services/ # business logic
└── main.py
```

Routes handle HTTP requests and responses. Services hold the actual logic. Models and schemas are kept separate from the API layer.

## Tech Stack
Python, FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Alembic, PyJWT, passlib (bcrypt), Pytest, httpx

## API & Security
- JWT authentication, role-based authorization
- Request and response validation with Pydantic
- Interactive docs via FastAPI's built-in Swagger UI

A few representative endpoints:
POST /auth/login
POST /servers
POST /servers/{id}/validation-runs
GET /findings


## Database
PostgreSQL stores servers, checks, validation runs, validation results, findings, users, and remediation records. SQLAlchemy handles queries, Alembic handles migrations.

## Core Workflow
An external validator submits results → ICCA checks each one against what's expected → a failed check opens a finding, or updates one that's already open instead of duplicating it → a passing check resolves it → remediation work can be tracked against the finding.

## Local Setup
```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Set up PostgreSQL, copy `.env.example` to `.env` and fill in your own values, then:
```powershell
alembic upgrade head
uvicorn app.main:app --reload
```

## Testing
```powershell
pytest -v
```
Tests cover authentication, role-based access, remediation status transitions, and the full validation-to-finding workflow.

## Out of Scope
ICCA doesn't:
- Connect to servers directly
- Run PowerShell, Bash, SSH, or WinRM
- Automatically remediate infrastructure
- Provision infrastructure

That's handled by separate automation tooling — ICCA only verifies, tracks, and reports.