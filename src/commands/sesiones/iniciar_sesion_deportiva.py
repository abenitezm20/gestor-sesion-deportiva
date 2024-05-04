import logging

from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.errors.errors import BadRequest
from src.models.sesion import EstadoSesionEnum, Sesion
from src.utils.str_utils import str_none_or_empty

logger = logging.getLogger(__name__)


class IniciarSesionDeportiva(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            logger.error('El email del deportista es requerido')
            raise BadRequest

        if str_none_or_empty(info.get('id_sesion')):
            logger.error('El id de la sesion es requerido')
            raise BadRequest

        self.email = info.get('email')
        self.id_sesion = info.get('id_sesion')

    def execute(self):
        with db_session() as session_db:

            sesion: Sesion = session_db.query(Sesion).filter(
                Sesion.id == self.id_sesion, Sesion.email == self.email).first()

            if not sesion:
                logger.error(
                    f'No se encontro la sesion con id {self.id_sesion} para el deportista {self.email}')
                raise BadRequest

            sesion.estado = EstadoSesionEnum.en_curso
            session_db.commit()

            resp = {
                'id_sesion': self.id_sesion,
                'estado': EstadoSesionEnum.en_curso.value,
            }

            return resp
