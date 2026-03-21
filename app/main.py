from fastapi import FastAPI

from .db import Base, engine
from . import models
from .routes.transactions import router as transactions_router

# Ensure SQLAlchemy models are registered before table creation.
_ = models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Transaction Review Service")
app.include_router(transactions_router)
