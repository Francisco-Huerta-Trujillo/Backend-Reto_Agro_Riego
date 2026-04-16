from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.alert import Alerta
from src.schemas.alert_schema import AlertCreate

class AlertService:
    # ------------------ CREATE ------------------
    # Este método generalmente NO lo llamará React. Lo llamará tu backend
    # internamente cuando evalúe la temperatura y humedad.
    @staticmethod
    async def create(db: AsyncSession, alert_in: AlertCreate) -> Alerta:
        db_alert = Alerta(**alert_in.model_dump())
        db.add(db_alert)
        await db.commit()
        await db.refresh(db_alert)
        return db_alert

    # ------------------ READ ------------------
    @staticmethod
    async def get_by_area(db: AsyncSession, id_areariego: UUID) -> list[Alerta]:
        # Para que en React, al darle clic a una granja, salgan sus alertas
        stmt = select(Alerta).where(Alerta.id_areariego == id_areariego).order_by(Alerta.fecha.desc())
        result = await db.execute(stmt)
        return list(result.scalars().all())

    # ------------------ DELETE (Limpiar bandeja) ------------------
    @staticmethod
    async def delete(db: AsyncSession, alert_id: int) -> bool:
        # Aquí sí permitimos borrar, por si el granjero quiere "Limpiar" sus notificaciones
        result = await db.execute(select(Alerta).where(Alerta.id == alert_id))
        db_alert = result.scalars().first()
        
        if not db_alert:
            return False
            
        await db.delete(db_alert)
        await db.commit()
        return True