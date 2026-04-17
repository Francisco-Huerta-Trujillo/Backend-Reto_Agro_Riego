from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID

from src.models.alert import Alerta
from src.schemas.alert_schema import AlertCreate

async def get_alerts(db: AsyncSession) -> list[Alerta]:
    result = await db.execute(select(Alerta).order_by(Alerta.fecha.desc()))
    return list(result.scalars().all())

async def get_alert(db: AsyncSession, alert_id: int) -> Alerta | None:
    result = await db.execute(select(Alerta).where(Alerta.id == alert_id))
    return result.scalars().first()

async def create_alert(db: AsyncSession, alert_in: AlertCreate) -> Alerta:
    db_alert = Alerta(**alert_in.model_dump())
    db.add(db_alert)
    await db.commit()
    await db.refresh(db_alert)
    return db_alert

async def mark_alert_as_read(db: AsyncSession, alert_id: int) -> bool:
    # Lógica para marcar como leída
    db_alert = await get_alert(db, alert_id)
    if not db_alert:
        return False
    # Asumiendo que agreguen una columna 'vista' en la BD
    # setattr(db_alert, 'vista', True) 
    await db.commit()
    return True

async def get_area_alerts(db: AsyncSession, area_id: UUID) -> list[Alerta]:
    result = await db.execute(select(Alerta).where(Alerta.id_areariego == area_id).order_by(Alerta.fecha.desc()))
    return list(result.scalars().all())