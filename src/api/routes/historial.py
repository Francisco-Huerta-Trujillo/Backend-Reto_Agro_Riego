from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.database.connection import get_db
from src.schemas.historial_schema import HistorialResponse
from src.services.historial_service import (
    get_historial, get_historial_item
)

router = APIRouter()

@router.get("/", response_model=List[HistorialResponse])
async def read_historial(db: AsyncSession = Depends(get_db)):
    return await get_historial(db)

@router.get("/{historial_id}", response_model=HistorialResponse)
async def read_historial_item(historial_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_historial_item(db, historial_id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return item