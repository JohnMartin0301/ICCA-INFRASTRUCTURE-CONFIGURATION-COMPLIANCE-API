from fastapi import FastAPI
from app.api import servers, checks, validation_runs, findings, auth, remediation


app = FastAPI(
    title="ICCA - Infrastructure Configuration & Compliance API",
    description="Tracks server configuration and compliance. An external process sends validation results, and ICCA tracks failed checks, open findings, and remediation work.",
    version="0.7.0"
)


app.include_router(servers.router)
app.include_router(checks.router)
app.include_router(validation_runs.router)
app.include_router(findings.router)
app.include_router(auth.router)
app.include_router(remediation.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}