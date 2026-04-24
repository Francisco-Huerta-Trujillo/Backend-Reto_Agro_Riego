from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime

class MedicionBase(BaseModel):
    # Agrega aquí el resto de variables de tu diagrama ER
    humedad_suelo: Optional[float] = None
    potencial_hidrico: Optional[float] = None
    temperatura_ambiente: Optional[float] = None
    radiacion_solar: Optional[float] = None

class MedicionCreate(MedicionBase):
    id_areariego: UUID # El sensor debe decir de qué área es
    # La fecha no se pide en el Create, la base de datos pondrá el CURRENT_TIMESTAMP sola

class MedicionResponse(BaseModel):
    id_areariego: UUID
    fecha: datetime
    humedad_suelo: Optional[float] = None
    potencial_hidrico: Optional[float] = None
    electroconductividad: Optional[float] = None
    temperatura_suelo: Optional[float] = None
    flujo_consumo_agua: Optional[float] = None
    temperatura_ambiente: Optional[float] = None
    humedad_relativa_ambiente: Optional[float] = None
    velocidad_viento: Optional[float] = None
    radiacion_solar: Optional[float] = None
    evapotranspiracion: Optional[float] = None

    class Config:
        from_attributes = True