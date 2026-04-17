from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.database.connection import get_db
from src.schemas.mediciones_schema import MedicionCreate, MedicionResponse
from src.services.mediciones_service import (
    get_mediciones, get_medicion, create_mediciones, get_area_mediciones
)

router = APIRouter()

@router.get("/", response_model=List[MedicionResponse])
async def read_mediciones(db: AsyncSession = Depends(get_db)):
    return await get_mediciones(db)

@router.get("/{medicion_id}", response_model=MedicionResponse)
async def read_medicion(medicion_id: int, db: AsyncSession = Depends(get_db)):
    medicion = await get_medicion(db, medicion_id)
    if not medicion:
        raise HTTPException(status_code=404, detail="Medición no encontrada")
    return medicion

@router.post("/", response_model=MedicionResponse)
async def create_mediciones_endpoint(mediciones: MedicionCreate, db: AsyncSession = Depends(get_db)):
    return await create_mediciones(db, mediciones)

@router.get("/area/{area_id}", response_model=List[MedicionResponse])
async def read_area_mediciones(area_id: UUID, db: AsyncSession = Depends(get_db)):
    return await get_area_mediciones(db, area_id)