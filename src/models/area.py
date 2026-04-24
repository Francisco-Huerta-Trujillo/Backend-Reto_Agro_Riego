# app/models/area.py (Incluye Predios según tu esquema)
from sqlalchemy import Column, String, ForeignKey, Table, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.database.base import Base

class AreaRiego(Base):
    __tablename__ = "areas_riego"

    id_areariego = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_predio = Column(UUID(as_uuid=True), ForeignKey("predios.id_predio", ondelete="CASCADE"))
    tipo_cultivo = Column(String(100))
    latitud = Column(Numeric(10, 8))
    longitud = Column(Numeric(11, 8))
    predio = relationship("Predio", back_populates="areas")