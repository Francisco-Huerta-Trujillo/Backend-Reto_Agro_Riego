from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import date

from src.database.connection import get_db
from src.schemas.predio_schema import PredioCreate, PredioUpdate, PredioResponse, DashboardStatsResponse, ChartConsumoResponse, ChartHumedadResponse
from src.schemas.area_schema import AreaResponse
from src.schemas.alert_schema import AlertResponse

from src.services.alert_service import get_predio_alerts
from src.services.predio_service import (
    get_predios, get_predio, create_predio, update_predio, delete_predio, get_predio_areas, get_dashboard_stats, get_chart_consumo, get_chart_humedad
)

from src.core.security import get_current_user

router = APIRouter()

@router.get("/")
async def read_predios(
    db: AsyncSession = Depends(get_db), 
    current_user = Depends(get_current_user) # Quitamos el tipo dict para evitar conflictos
):
    try:
        # Intentamos sacar el ID de todas las formas posibles que usa FastAPI
        u_id = None
        
        if isinstance(current_user, dict):
            u_id = current_user.get("user_id") or current_user.get("id") or current_user.get("sub")
        else:
            u_id = getattr(current_user, "id_usuario", None) or getattr(current_user, "id", None)

        if not u_id:
            print("🚨 ERROR: No se encontró ID en el token. Contenido:", current_user)
            raise HTTPException(status_code=401, detail="Token inválido")

        return await get_predios(u_id, db)
        
    except Exception as e:
        print(f"🔥 ERROR CRÍTICO EN PREDIOS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{predio_id}", response_model=PredioResponse)
async def read_predio(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    predio = await get_predio(db, predio_id)
    if not predio:
        raise HTTPException(status_code=404, detail="Predio no encontrado")
    return predio

@router.post("/", response_model=PredioResponse)
async def create_predio_endpoint(predio: PredioCreate, db: AsyncSession = Depends(get_db)):
    return await create_predio(db, predio)

@router.put("/{predio_id}", response_model=PredioResponse)
async def update_predio_endpoint(predio_id: UUID, predio: PredioUpdate, db: AsyncSession = Depends(get_db)):
    predio_actualizado = await update_predio(db, predio_id, predio)
    if not predio_actualizado:
        raise HTTPException(status_code=404, detail="Predio no encontrado")
    return predio_actualizado

@router.delete("/{predio_id}")
async def delete_predio_endpoint(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    exito = await delete_predio(db, predio_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Predio no encontrado")
    return {"mensaje": "Predio eliminado exitosamente"}

@router.get("/{predio_id}/areas", response_model=List[AreaResponse])
async def read_predio_areas(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_predio_areas(db, predio_id)

@router.get("/{predio_id}/dashboard-stats", response_model=DashboardStatsResponse)
async def read_dashboard_stats(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db, predio_id)

@router.get("/{predio_id}/chart-humedad", response_model=List[ChartHumedadResponse])
async def read_chart_humedad(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_chart_humedad(db, predio_id)

@router.get("/{predio_id}/chart-consumo", response_model=List[ChartConsumoResponse])
async def read_chart_consumo(
    predio_id: UUID, 
    start_date: date = None, # Parámetro opcional en la URL
    end_date: date = None,   # Parámetro opcional en la URL
    db: AsyncSession = Depends(get_db)
):
    return await get_chart_consumo(db, predio_id, start_date, end_date)

@router.get("/{predio_id}/alerts", response_model=List[AlertResponse])
async def read_predio_alerts(predio_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_predio_alerts(db, predio_id)