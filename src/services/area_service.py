from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.area import AreaRiego
from src.models.alert import Alerta
from src.models.mediciones import Medicion
from src.schemas.area_schema import AreaCreate, AreaUpdate

async def get_areas(db: AsyncSession) -> list[AreaRiego]:
    result = await db.execute(select(AreaRiego))
    return list(result.scalars().all())

async def get_area(db: AsyncSession, area_id: UUID) -> AreaRiego | None:
    result = await db.execute(select(AreaRiego).where(AreaRiego.id_areariego == area_id))
    return result.scalars().first()

async def create_area(db: AsyncSession, area_in: AreaCreate) -> AreaRiego:
    db_area = AreaRiego(**area_in.model_dump())
    db.add(db_area)
    await db.commit()
    await db.refresh(db_area)
    return db_area

async def update_area(db: AsyncSession, area_id: UUID, area_in: AreaUpdate) -> AreaRiego | None:
    db_area = await get_area(db, area_id)
    if not db_area: return None
    update_data = area_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_area, key, value)
    await db.commit()
    await db.refresh(db_area)
    return db_area

async def delete_area(db: AsyncSession, area_id: UUID) -> bool:
    db_area = await get_area(db, area_id)
    if not db_area: return False
    await db.delete(db_area)
    await db.commit()
    return True

async def get_area_sensors(db: AsyncSession, area_id: UUID, limite: int = 100) -> list[Medicion]:
    # Traemos las últimas 100 mediciones de esta área para graficar
    stmt = select(Medicion).where(Medicion.id_areariego == area_id).order_by(Medicion.fecha.desc()).limit(limite)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_area_alerts(db: AsyncSession, area_id: UUID) -> list[Alerta]:
    # Traemos todas las alertas de esta área, las más recientes primero
    stmt = select(Alerta).where(Alerta.id_areariego == area_id).order_by(Alerta.fecha.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())