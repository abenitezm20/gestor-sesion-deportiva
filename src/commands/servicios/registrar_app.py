import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import AppRegistrada, BadRequest
from src.models.app_externa import AppExterna, EstadoAppExternaEnum
from src.models.db import db_session
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class RegistrarApp(BaseCommand):

    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            logger.error('El email del deportista es requerido')
            raise BadRequest('El email del deportista es requerido')

        if str_none_or_empty(info.get('nombre')):
            logger.error('El nombre de la app es requerido')
            raise BadRequest('El nombre de la app es requerido')

        if str_none_or_empty(info.get('descripcion')):
            logger.error('La descripcion de la app es requerida')
            raise BadRequest('La descripcion de la app es requerida')

        if str_none_or_empty(info.get('webhook')):
            logger.error('El webhook de la app es requerido')
            raise BadRequest('El webhook de la app es requerido')

        if str_none_or_empty(info.get('token')):
            logger.error('El token de la app es requerido')
            raise BadRequest('El token de la app es requerido')

        self.email = info.get('email')
        self.nombre = info.get('nombre')
        self.descripcion = info.get('descripcion')
        self.webhook = info.get('webhook')
        self.token = info.get('token')

    def execute(self):
        logger.info('Registrando app para el deportista %s', self.email)

        app_externa = AppExterna.query.filter(
            AppExterna.email == self.email,
            AppExterna.nombre == self.nombre).first()

        if app_externa:
            logger.error('Ya existe una app con el nombre proporcionado')
            raise AppRegistrada

        with db_session() as session:

            app: AppExterna = AppExterna(
                nombre=self.nombre,
                descripcion=self.descripcion,
                estado=EstadoAppExternaEnum.activa,
                webhook=self.webhook,
                token=self.token,
                email=self.email)

            session.add(app)
            session.commit()
            logger.info(f'Aplicación externa registrada {app.id}')

            resp = {
                'id': str(app.id),
                'estado': app.estado
            }

            return resp
