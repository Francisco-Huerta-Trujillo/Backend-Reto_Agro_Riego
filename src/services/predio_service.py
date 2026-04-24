from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete, func, cast, Date
from sqlalchemy.orm import selectinload
from uuid import UUID
from typing import List

from src.models.predio import Predio
from src.models.associations import usuarios_predios
from src.schemas.predio_schema import PredioCreate, PredioUpdate
from src.models.mediciones import Medicion
from src.models.area import AreaRiego

async def get_predios(usuario_id: str, db: AsyncSession) -> list[Predio]:
    stmt = (
        select(Predio)
        .options(selectinload(Predio.areas)) # 👈 ✨ ESTA ES LA MAGIA ✨
        .join(usuarios_predios, Predio.id_predio == usuarios_predios.c.id_predio)
        .where(usuarios_predios.c.id_usuario == usuario_id)
    )
    
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_predio(db: AsyncSession, predio_id: UUID) -> Predio | None:
    result = await db.execute(select(Predio).where(Predio.id_predio == predio_id))
    return result.scalars().first()

async def create_predio(db: AsyncSession, predio_in: PredioCreate) -> Predio:
    db_predio = Predio(**predio_in.model_dump())
    db.add(db_predio)
    await db.commit()
    await db.refresh(db_predio)
    return db_predio

async def update_predio(db: AsyncSession, predio_id: UUID, predio_in: PredioUpdate) -> Predio | None:
    db_predio = await get_predio(db, predio_id)
    if not db_predio: return None
    update_data = predio_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_predio, key, value)
    await db.commit()
    await db.refresh(db_predio)
    return db_predio

async def delete_predio(db: AsyncSession, predio_id: UUID) -> bool:
    db_predio = await get_predio(db, predio_id)
    if not db_predio: return False
    await db.delete(db_predio)
    await db.commit()
    return True

async def get_predio_areas(db: AsyncSession, predio_id: UUID):
    # Esto deberá devolver las áreas del predio
    from src.models.area import AreaRiego
    result = await db.execute(select(AreaRiego).where(AreaRiego.id_predio == predio_id))
    return list(result.scalars().all())

async def asignar_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
    stmt = insert(usuarios_predios).values(id_usuario=id_usuario, id_predio=id_predio)
    try:
        await db.execute(stmt)
        await db.commit()
        return True
    except Exception:
        # Si da error (ej. el usuario ya estaba asignado), hacemos rollback para no trabar la base de datos
        await db.rollback()
        return False

async def remover_usuario(db: AsyncSession, id_predio: UUID, id_usuario: UUID) -> bool:
    stmt = delete(usuarios_predios).where(
        usuarios_predios.c.id_usuario == id_usuario,
        usuarios_predios.c.id_predio == id_predio
    )
    await db.execute(stmt)
    await db.commit()
    return True

async def get_dashboard_stats(db: AsyncSession, predio_id: UUID):
    # 1. Hacemos la consulta uniendo Mediciones con AreasRiego
    query = (
        select(
            func.avg(Medicion.humedad_suelo),
            func.avg(Medicion.temperatura_ambiente),
            func.avg(Medicion.evapotranspiracion),
            func.sum(Medicion.flujo_consumo_agua)
        )
        .join(AreaRiego, Medicion.id_areariego == AreaRiego.id_areariego)
        .where(AreaRiego.id_predio == predio_id)
    )
    
    result = await db.execute(query)
    row = result.first()

    # 2. Si el predio es nuevo y no tiene mediciones, devolvemos ceros
    if not row or row[0] is None:
        return {
            "soil_humidity": "0",
            "ambient_temp": "0",
            "evapotranspiration": "0",
            "water_consumption": "0"
        }

    # 3. Formateamos los números a 1 decimal
    return {
        "soil_humidity": f"{row[0]:.1f}",
        "ambient_temp": f"{row[1]:.1f}",
        "evapotranspiration": f"{row[2]:.1f}",
        "water_consumption": f"{row[3]:.1f}"
    }

async def get_chart_humedad(db: AsyncSession, predio_id: UUID) -> List[dict]:
    # Expresión segura para agrupar por hora
    hora_expr = func.to_char(Medicion.fecha, 'HH24:00')
    
    query = (
        select(
            hora_expr,
            func.avg(Medicion.humedad_suelo)
        )
        .join(AreaRiego, Medicion.id_areariego == AreaRiego.id_areariego)
        .where(AreaRiego.id_predio == predio_id)
        .group_by(hora_expr)
        .order_by(hora_expr)
    )
    
    result = await db.execute(query)
    rows = result.all()

    return [{"time": row[0], "value": float(f"{row[1]:.1f}")} for row in rows if row[1] is not None]

async def get_chart_consumo(db: AsyncSession, predio_id: UUID) -> List[dict]:
    # Expresiones seguras para agrupar por día
    dia_expr = func.to_char(Medicion.fecha, 'Dy')
    fecha_pura_expr = cast(Medicion.fecha, Date)
    
    query = (
        select(
            dia_expr,
            func.sum(Medicion.flujo_consumo_agua)
        )
        .join(AreaRiego, Medicion.id_areariego == AreaRiego.id_areariego)
        .where(AreaRiego.id_predio == predio_id)
        .group_by(dia_expr, fecha_pura_expr)
        .order_by(fecha_pura_expr)
        .limit(7)
    )
    
    result = await db.execute(query)
    rows = result.all()

    return [{"day": row[0], "value": float(f"{row[1]:.1f}")} for row in rows if row[1] is not None]