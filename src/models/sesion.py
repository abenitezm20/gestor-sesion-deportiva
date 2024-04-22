import enum

from .db import Base
from sqlalchemy import UUID, Column, DateTime, Enum
from src.models.model import Model


class EstadoSesionEnum(str, enum.Enum):
    agendada = "agendado"
    en_curso = "en_curso"
    finalizada = "finalizada"


class Sesion(Model, Base):
    __tablename__ = "sesion"
    id_plan_deportista = Column(UUID(as_uuid=True))
    estado = Column(Enum(EstadoSesionEnum))
    fecha_inicio = Column(DateTime)

    def __init__(self, id_plan_deportista, estado, fecha_inicio):
        Model.__init__(self)
        self.id_plan_deportista = id_plan_deportista
        self.estado = estado
        self.fecha_inicio = fecha_inicio
