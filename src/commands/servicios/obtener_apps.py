import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.app_externa import AppExterna
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerApps(BaseCommand):

    def __init__(self, **info):
        if str_none_or_empty(info.get('email')):
            raise BadRequest('El email del deportista es requerido')

        self.email = info.get('email')

    def execute(self):
        logger.info('Obteniendo apps del deportista %s', self.email)

        apps_deportista = AppExterna.query.filter(
            AppExterna.email == self.email).all()

        resp = []

        app: AppExterna
        for app in apps_deportista:
            app_info = {
                'id': app.id,
                'nombre': app.nombre,
                'descripcion': app.descripcion,
                'estado': app.estado.value,
                'webhook': app.webhook,
                'token': app.token,
                'fecha_modificacion': app.updated_at.strftime("%Y-%m-%dT%H:%M:%S")
            }
            resp.append(app_info)

        return resp
