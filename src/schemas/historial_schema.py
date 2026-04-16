from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class HistorialBase(BaseModel):
    ajuste_realizado: str  # Ej: "El usuario cambió la contraseña" o "Modificó el área 1"

class HistorialCreate(HistorialBase):
    id_usuario: UUID  # Necesitamos saber quién hizo el cambio

class HistorialResponse(HistorialBase):
    id: int
    id_usuario: UUID
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)