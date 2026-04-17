from fastapi import APIRouter

from src.api.routes import users, predios, areas, mediciones, alerts, historial

api_router = APIRouter()

api_router.include_router(users.router, prefix="/usuarios", tags=["Gestión de Usuarios"])
api_router.include_router(predios.router, prefix="/predios", tags=["Gestión de Predios"])
api_router.include_router(areas.router, prefix="/areas", tags=["Áreas de Riego"])
api_router.include_router(mediciones.router, prefix="/mediciones", tags=["Telemetría IoT (Mediciones)"])
api_router.include_router(alerts.router, prefix="/alertas", tags=["Sistema de Alertas"])
api_router.include_router(historial.router, prefix="/historial", tags=["Auditoría e Historial"])