from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional, List # Importamos List
from uuid import UUID
# IMPORTANTE: Importas el esquema del otro archivo
from src.schemas.area_schema import AreaResponse 

class PredioBase(BaseModel):
    coordenadas: Optional[str] = None
    id_encargado: Optional[UUID] = None

class PredioResponse(PredioBase):
    id_predio: UUID
    lat: float = 0.0
    lng: float = 0.0
    # Aquí usas la clase que importaste arriba
    areas: List[AreaResponse] = [] 

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode='after')
    def split_coordenadas(self) -> 'PredioResponse':
        if self.coordenadas and ',' in self.coordenadas:
            try:
                parts = self.coordenadas.split(',')
                self.lat = float(parts[0].strip())
                self.lng = float(parts[1].strip())
            except:
                self.lat, self.lng = 0.0, 0.0
        return self
    
# 2. Create: Lo que pedimos para registrar un nuevo predio
class PredioCreate(PredioBase):
    pass # No hay campos extra obligatorios para crear, hereda todo de Base

# 3. Update: Lo que pedimos para actualizar (todo opcional)
class PredioUpdate(BaseModel):
    coordenadas: Optional[str] = None
    id_encargado: Optional[UUID] = None

# 4. Response: Lo que le devolvemos a React
class PredioResponse(PredioBase):
    id_predio: UUID

    # Permite a Pydantic leer el objeto directamente de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)

class UsuarioPredioAsignacion(BaseModel):
    id_usuario: UUID
    id_predio: UUID

class DashboardStatsResponse(BaseModel):
    soil_humidity: str
    ambient_temp: str
    evapotranspiration: str
    water_consumption: str

class ChartHumedadResponse(BaseModel):
    time: str
    value: float

class ChartConsumoResponse(BaseModel):
    day: str
    value: float