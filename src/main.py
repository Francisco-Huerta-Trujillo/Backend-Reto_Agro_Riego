from fastapi import FastAPI
from src.api.api import api_router

app = FastAPI(
    title="AgroRiego API",
    description="API para gestión y monitoreo inteligente de riego agrícola.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api/v1")