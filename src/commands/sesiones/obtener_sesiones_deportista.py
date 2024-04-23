import datetime
import logging

from sqlalchemy import func
from datetime import datetime
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, SesionYaAgendada
from src.models.db import db_session
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import EstadoSesionEnum, Sesion
from src.utils.seguridad_utils import UsuarioToken
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerSesionesDeportista(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            raise BadRequest('El email del deportista es requerido')

        self.email = info.get('email')
        self.fecha = info.get('fecha')

    def execute(self):
        resultados = []

        if self.fecha is not None:
            logger.info(
                f'Consultando resultado sesiones del deportista {self.email} para la fecha {self.fecha}')
            resultados = self._consulta_por_fecha()
        else:
            logger.info(
                f'Consultando resultado sesiones del deportista {self.email}')
            resultados = self._consulta_todas()

        resp = []
        tmp: ResultadoSesion
        for tmp in resultados:
            resultado = {
                'fecha_inicio': tmp.fecha_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                'fecha_fin': tmp.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"),
                'vo2_max': tmp.vo2_max,
                'ftp': tmp.ftp,
                'estado': tmp.sesion.estado
            }
            resp.append(resultado)

        return resp

    def _consulta_por_fecha(self):

        filtro_fecha = datetime.fromisoformat(self.fecha)
        año = filtro_fecha.year
        mes = filtro_fecha.month

        resultados_mes = ResultadoSesion.query.join(Sesion).filter(
            Sesion.email == self.email,
            func.extract('year', Sesion.fecha_sesion) == año,
            func.extract('month', Sesion.fecha_sesion) == mes
        ).all()

        return resultados_mes

    def _consulta_todas(self):
        resultados = ResultadoSesion.query.join(Sesion).filter(
            Sesion.email == self.email).all()

        return resultados
