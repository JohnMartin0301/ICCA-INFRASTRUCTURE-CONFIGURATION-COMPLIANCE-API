from fastapi import FastAPI
from app.api import servers

app = FastAPI(title="ICCA - Infrastructure Configuration & Compliance API")

app.include_router(servers.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}