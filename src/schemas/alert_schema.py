from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class AlertBase(BaseModel):
    tipo_de_alerta: str    # Ej: "ESTRES_HIDRICO", "SATURACION", "SENSOR_OFFLINE"
    mensaje_de_alerta: str # Ej: "La humedad cayó al 15%, iniciar riego de inmediato."

class AlertCreate(AlertBase):
    id_areariego: UUID

class AlertResponse(AlertBase):
    id: int
    id_areariego: UUID
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)