from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.mediciones import Medicion
from src.schemas.mediciones_schema import MedicionCreate

async def get_mediciones(db: AsyncSession, limite: int = 100) -> list[Medicion]:
    result = await db.execute(select(Medicion).order_by(Medicion.fecha.desc()).limit(limite))
    return list(result.scalars().all())

async def get_medicion(db: AsyncSession, medicion_id: int) -> Medicion | None:
    result = await db.execute(select(Medicion).where(Medicion.id == medicion_id))
    return result.scalars().first()

async def create_mediciones(db: AsyncSession, medicion_in: MedicionCreate) -> Medicion:
    db_medicion = Medicion(**medicion_in.model_dump())
    db.add(db_medicion)
    await db.commit()
    await db.refresh(db_medicion)
    return db_medicion

async def get_area_mediciones(db: AsyncSession, area_id: UUID, limite: int = 100) -> list[Medicion]:
    stmt = select(Medicion).where(Medicion.id_areariego == area_id).order_by(Medicion.fecha.desc()).limit(limite)
    result = await db.execute(stmt)
    return list(result.scalars().all())