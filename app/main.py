from fastapi import FastAPI

from .db import Base, engine
from . import models
from .routes.transactions import router as transactions_router
from .schemas import HealthCheckResponse

# Ensure SQLAlchemy models are registered before table creation.
_ = models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transaction Review Service")
app.include_router(transactions_router)


@app.get("/", response_model=HealthCheckResponse)
def health_check() -> HealthCheckResponse:
    return {"message": "Transaction Review Service is running. See /docs for API usage."}
