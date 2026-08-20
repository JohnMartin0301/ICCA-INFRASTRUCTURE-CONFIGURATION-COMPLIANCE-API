from fastapi import FastAPI
from app.api import servers, checks, validation_runs, findings, auth


app = FastAPI(title="ICCA - Infrastructure Configuration & Compliance API")


app.include_router(servers.router)
app.include_router(checks.router)
app.include_router(validation_runs.router)
app.include_router(findings.router)
app.include_router(auth.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}