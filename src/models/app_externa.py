import enum

from sqlalchemy import Column, Enum, String

from src.models.db import Base
from src.models.model import Model


class EstadoAppExternaEnum(str, enum.Enum):
    activa = "Activa"
    inactiva = "Inactiva"


class AppExterna(Model, Base):
    __tablename__ = "app_externas"
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(200), nullable=False)
    estado = Column(Enum(EstadoAppExternaEnum), nullable=False)
    webhook = Column(String(2083), nullable=False)
    token = Column(String(2000), nullable=False)
    email = Column(String(50), nullable=False)

    def __init__(self, nombre, descripcion, estado: EstadoAppExternaEnum, webhook, token, email):
        Model.__init__(self)
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado.value
        self.webhook = webhook
        self.token = token
        self.email = email
