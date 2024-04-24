import logging

from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import Sesion
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerEstadisticasDeportista(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            raise BadRequest('El email del deportista es requerido')

        self.email = info.get('email')

    def execute(self):

        resultados = ResultadoSesion.query.join(Sesion).filter(
            Sesion.email == self.email).all()

        lista_ftp = []
        lista_vo2 = []

        resultado: ResultadoSesion
        for resultado in resultados:
            ftp = {
                'fecha': resultado.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"),
                'valor': resultado.ftp
            }
            lista_ftp.append(ftp)

            vo2 = {
                'fecha': resultado.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"),
                'valor': resultado.vo2_max
            }
            lista_vo2.append(vo2)

        resp = {
            'ftp': lista_ftp,
            'vo2': lista_vo2
        }

        return resp
