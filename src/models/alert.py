# app/models/alert.py
from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database.base import Base

class Alerta(Base):
    __tablename__ = "alertas"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_areariego = Column(UUID(as_uuid=True), ForeignKey("areas_riego.id_areariego", ondelete="CASCADE"))
    tipo_de_alerta = Column(String(100), nullable=False)
    mensaje_de_alerta = Column(Text, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())