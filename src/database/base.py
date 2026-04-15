# app/database/base.py
from sqlalchemy.orm import declarative_base

# Clase base que heredan todos tus modelos
Base = declarative_base()