from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.historial import HistorialCambios
from src.schemas.historial_schema import HistorialCreate

async def get_historial(db: AsyncSession, limite: int = 50) -> list[HistorialCambios]:
    result = await db.execute(select(HistorialCambios).order_by(HistorialCambios.fecha.desc()).limit(limite))
    return list(result.scalars().all())

async def get_historial_item(db: AsyncSession, historial_id: int) -> HistorialCambios | None:
    result = await db.execute(select(HistorialCambios).where(HistorialCambios.id == historial_id))
    return result.scalars().first()

async def create(db: AsyncSession, historial_in: HistorialCreate) -> HistorialCambios:
    db_historial = HistorialCambios(**historial_in.model_dump())
    db.add(db_historial)
    await db.commit()
    await db.refresh(db_historial)
    return db_historial