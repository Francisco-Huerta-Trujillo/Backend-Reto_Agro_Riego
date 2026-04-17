# app/models/historial.py
from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database.base import Base

class HistorialCambios(Base):
    __tablename__ = "historial_cambios"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="CASCADE"))
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    ajuste_realizado = Column(Text, nullable=False)