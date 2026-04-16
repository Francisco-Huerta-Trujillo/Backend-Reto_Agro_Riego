# app/models/mediciones.py
from sqlalchemy import Column, BigInteger, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.base import Base

class Medicion(Base):
    __tablename__ = "mediciones"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_areariego = Column(UUID(as_uuid=True), ForeignKey("areas_riego.id_areariego", ondelete="CASCADE"))
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    
    # Datos de suelo
    humedad_suelo = Column(Float)
    potencial_hidrico = Column(Float)
    electroconductividad = Column(Float)
    temperatura_suelo = Column(Float)
    
    # Datos de ambiente e hídricos
    flujo_consumo_agua = Column(Float)
    temperatura_ambiente = Column(Float)
    humedad_relativa_ambiente = Column(Float)
    velocidad_viento = Column(Float)
    radiacion_solar = Column(Float)
    evapotranspiracion = Column(Float)