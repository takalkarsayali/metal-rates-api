
from fastapi import FastAPI
from app.routers import rates

app = FastAPI(
    title="Live Metal Rates API",
    description="Centralized API for retrieving live and historical precious metal rates.",
    version="1.0.0"
)

app.include_router(rates.router)


@app.get("/", tags=["General"])
def root():
    return {
        "application": "Live Metal Rates API",
        "status": "running",
        "documentation": "/docs"
    }


@app.get("/health", tags=["General"])
def health_check():
    return {"status": "healthy"}
