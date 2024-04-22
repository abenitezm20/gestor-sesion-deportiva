from src.models.sesion import Sesion
from .db import Base
from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship
from src.models.model import Model


class ResultadoSesion(Model, Base):
    __tablename__ = "resultado_sesion"
    id_sesion = Column(UUID(as_uuid=True), ForeignKey('sesion.id'), primary_key=True)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    vo2_max = Column(Integer)
    ftp = Column(Integer)

    sesion: Mapped['Sesion'] = relationship("Sesion")

    def __init__(self, id_sesion, fecha_inicio, fecha_fin, vo2_max, ftp):
        Model.__init__(self)
        self.id_sesion = id_sesion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.vo2_max = vo2_max
        self.ftp = ftp
