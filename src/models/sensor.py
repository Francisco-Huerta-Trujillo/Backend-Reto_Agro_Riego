# app/models/sensor.py
from sqlalchemy import Column, Float, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.base import Base

class Medicion(Base):
    __tablename__ = "mediciones"
    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas_riego.id"))
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    humedad = Column(Float)
    temperatura = Column(Float)