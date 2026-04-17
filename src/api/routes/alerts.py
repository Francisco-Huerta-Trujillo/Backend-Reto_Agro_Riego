from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.schemas.alert_schema import AlertCreate, AlertResponse
from src.services.alert_service import (
    get_alerts, get_alert, create_alert, mark_alert_as_read, get_area_alerts
)

router = APIRouter()

@router.get("/", response_model=List[AlertResponse])
async def read_alerts(db: AsyncSession = Depends(get_db)):
    return await get_alerts(db)

@router.get("/{alert_id}", response_model=AlertResponse)
async def read_alert(alert_id: int, db: AsyncSession = Depends(get_db)):
    alert = await get_alert(db, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alert

@router.post("/", response_model=AlertResponse)
async def create_alert_endpoint(alert: AlertCreate, db: AsyncSession = Depends(get_db)):
    return await create_alert(db, alert)

@router.put("/{alert_id}/read")
async def mark_as_read(alert_id: int, db: AsyncSession = Depends(get_db)):
    exito = await mark_alert_as_read(db, alert_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return {"mensaje": "Alerta marcada como leída"}

@router.get("/area/{area_id}", response_model=List[AlertResponse])
async def read_area_alerts(area_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_area_alerts(db, area_id)