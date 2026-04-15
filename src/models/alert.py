# app/models/alert.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.base import Base

class Alerta(Base):
    __tablename__ = "alertas"
    id = Column(Integer, primary_key=True, index=True)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas_riego.id"))
    medicion_id = Column(Integer, ForeignKey("mediciones.id"))
    tipo_alerta = Column(String)
    mensaje = Column(String)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    vista = Column(Boolean, default=False)