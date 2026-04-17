from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.schemas.predio_schema import PredioCreate, PredioUpdate, PredioResponse
from src.schemas.area_schema import AreaResponse
from src.services.predio_service import (
    get_predios, get_predio, create_predio, update_predio, delete_predio, get_predio_areas
)

router = APIRouter()

@router.get("/", response_model=List[PredioResponse])
async def read_predios(db: AsyncSession = Depends(get_db)):
    return await get_predios(db)

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