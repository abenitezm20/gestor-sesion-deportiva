import enum

from .db import Base
from sqlalchemy import UUID, Column, DateTime, Enum, String
from src.models.model import Model


class EstadoSesionEnum(str, enum.Enum):
    agendada = "agendada"
    en_curso = "en_curso"
    finalizada = "finalizada"


class Sesion(Model, Base):
    __tablename__ = "sesion"
    id_plan_deportista = Column(UUID(as_uuid=True))
    email = Column(String(50), unique=False)
    estado = Column(Enum(EstadoSesionEnum))
    fecha_sesion = Column(DateTime)

    def __init__(self, id_plan_deportista, email, estado: EstadoSesionEnum, fecha_sesion):
        Model.__init__(self)
        self.id_plan_deportista = id_plan_deportista
        self.email = email
        self.estado = estado.value
        self.fecha_sesion = fecha_sesion
