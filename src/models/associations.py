from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base import Base

usuarios_predios = Table(
    "usuarios_predios",
    Base.metadata,
    Column("id_usuario", UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), primary_key=True),
    Column("id_predio", UUID(as_uuid=True), ForeignKey("predios.id_predio", ondelete="CASCADE"), primary_key=True),
)