import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.errors.errors import BadRequest
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import EstadoSesionEnum, Sesion
from src.utils.str_utils import str_none_or_empty

logger = logging.getLogger(__name__)


class FinalizarSesionDeportiva(BaseCommand):
    def __init__(self, **info):
        if str_none_or_empty(info.get('email')):
            logger.error('El email del deportista es requerido')
            raise BadRequest

        if str_none_or_empty(info.get('id_sesion')):
            logger.error('El id de la sesion es requerido')
            raise BadRequest

        if info.get('vo2_max') is None:
            logger.error('El vo2 max es requerido')
            raise BadRequest

        if info.get('ftp') is None:
            logger.error('El ftp es requerido')
            raise BadRequest

        if str_none_or_empty(info.get('fecha_inicio')):
            logger.error('La fecha de inicio es requerida')
            raise BadRequest

        if str_none_or_empty(info.get('fecha_fin')):
            logger.error('La fecha de fin es requerida')
            raise BadRequest

        self.email = info.get('email')
        self.id_sesion = info.get('id_sesion')
        self.vo2_max = info.get('vo2_max')
        self.ftp = info.get('ftp')
        self.fecha_inicio = info.get('fecha_inicio')
        self.fecha_fin = info.get('fecha_fin')

    def execute(self):
        with db_session() as session_db:

            sesion: Sesion = session_db.query(Sesion).filter(
                Sesion.id == self.id_sesion, Sesion.email == self.email).first()

            if not sesion:
                logger.error(
                    f'No se encontro la sesion con id {self.id_sesion} para el deportista {self.email}')
                raise BadRequest

            sesion.estado = EstadoSesionEnum.finalizada

            resultado_sesion: ResultadoSesion = ResultadoSesion(
                id_sesion=self.id_sesion,
                vo2_max=self.vo2_max,
                ftp=self.ftp,
                fecha_inicio=self.fecha_inicio,
                fecha_fin=self.fecha_fin,
            )
            session_db.add(resultado_sesion)
            session_db.commit()

            resp = {
                'id_sesion': self.id_sesion,
                'estado': EstadoSesionEnum.finalizada.value,
            }

            return resp
