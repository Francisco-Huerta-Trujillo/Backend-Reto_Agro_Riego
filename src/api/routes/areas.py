from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.schemas.area_schema import AreaCreate, AreaUpdate, AreaResponse
from src.schemas.mediciones_schema import MedicionResponse
from src.schemas.alert_schema import AlertResponse
from src.services.area_service import (
    get_areas, get_area, create_area, update_area, delete_area, get_area_sensors, get_area_alerts
)

router = APIRouter()

@router.get("/", response_model=List[AreaResponse])
async def read_areas(db: AsyncSession = Depends(get_db)):
    return await get_areas(db)

@router.get("/{area_id}", response_model=AreaResponse)
async def read_area(area_id: UUID, db: AsyncSession = Depends(get_db)):
    area = await get_area(db, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return area

@router.post("/", response_model=AreaResponse)
async def create_area_endpoint(area: AreaCreate, db: AsyncSession = Depends(get_db)):
    return await create_area(db, area)

@router.put("/{area_id}", response_model=AreaResponse)
async def update_area_endpoint(area_id: UUID, area: AreaUpdate, db: AsyncSession = Depends(get_db)):
    area_actualizada = await update_area(db, area_id, area)
    if not area_actualizada:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return area_actualizada

@router.delete("/{area_id}")
async def delete_area_endpoint(area_id: UUID, db: AsyncSession = Depends(get_db)):
    exito = await delete_area(db, area_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Área no encontrada")
    return {"mensaje": "Área eliminada exitosamente"}

@router.get("/{area_id}/sensors", response_model=List[MedicionResponse])
async def read_area_sensors(area_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_area_sensors(db, area_id)

@router.get("/{area_id}/alerts", response_model=List[AlertResponse])
async def read_area_alerts(area_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_area_alerts(db, area_id)