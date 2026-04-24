from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from src.models.mediciones import Medicion
from src.models.alert import Alerta
from src.schemas.mediciones_schema import MedicionCreate
from src.utils.alert_validator import check_for_alerts

async def get_mediciones(db: AsyncSession, limite: int = 100) -> list[Medicion]:
    result = await db.execute(select(Medicion).order_by(Medicion.fecha.desc()).limit(limite))
    return list(result.scalars().all())

async def get_medicion(db: AsyncSession, medicion_id: int) -> Medicion | None:
    result = await db.execute(select(Medicion).where(Medicion.id == medicion_id))
    return result.scalars().first()

async def create_mediciones(db: AsyncSession, payload: dict) -> Medicion:
    # 1. Evaluamos las alertas con tu helper
    nuevas_alertas = check_for_alerts(payload)
    
    # 2. Preparamos las alertas en la base de datos
    for alerta_data in nuevas_alertas:
        db.add(Alerta(**alerta_data))

    # 3. Aplanamos el JSON para la tabla de Mediciones
    sensor_data = payload.get("sensor_data", {})
    environment = sensor_data.get("environment", {})
    soil = sensor_data.get("soil", {})
    
    # Pasamos los datos por tu esquema para validarlos
    medicion_plana = MedicionCreate(
        id_areariego=payload.get("metadata", {}).get("id_areariego"),
        humedad_suelo=soil.get("moisture", 0.0),
        temperatura_ambiente=environment.get("air_temp", 0.0),
        evapotranspiracion=environment.get("et0", 0.0),
        # Extraemos del status si existe
        flujo_consumo_agua=payload.get("status", {}).get("water_consumption", 0.0)
        # (Añade aquí cualquier otro campo que requiera tu MedicionCreate)
    )

    # 4. Preparamos la medición
    db_medicion = Medicion(**medicion_plana.model_dump())
    db.add(db_medicion)

    # 5. Guardamos TODO junto en una sola transacción segura
    await db.commit()
    await db.refresh(db_medicion)
    
    return db_medicion

async def get_area_mediciones(db: AsyncSession, area_id: UUID, limite: int = 100) -> list[Medicion]:
    stmt = select(Medicion).where(Medicion.id_areariego == area_id).order_by(Medicion.fecha.desc()).limit(limite)
    result = await db.execute(stmt)
    return list(result.scalars().all())