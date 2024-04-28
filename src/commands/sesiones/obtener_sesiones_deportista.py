import logging


from sqlalchemy import text
from src.commands.base_command import BaseCommand
from src.models.db import db_session
from src.errors.errors import BadRequest
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import Sesion
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class ObtenerSesionesDeportista(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('email')):
            raise BadRequest('El email del deportista es requerido')

        self.email = info.get('email')

    def execute(self):
        resultados = self._consulta_todas()

        resp = []
        tmp: ResultadoSesion
        for tmp in resultados:
            resultado = {
                'id_plan_deportista': tmp.id_plan_deportista,
                'fecha_inicio': tmp.resultado_fecha_inicio,
                'fecha_fin': tmp.resultado_fecha_fin,
                'vo2_max': tmp.vo2_max,
                'ftp': tmp.ftp,
                'estado': tmp.estado_sesion,
                'fecha_sesion': tmp.fecha_sesion
            }
            resp.append(resultado)

        return resp

    def _consulta_todas(self):
        query = """
            select
                s.id_plan_deportista id_plan_deportista,
                s.estado estado_sesion,
                to_char(s.fecha_sesion, 'YYYY-MM-DD"T"HH24:MI:SS') fecha_sesion,
                rs.vo2_max vo2_max,
                rs.ftp ftp,
                to_char(rs.fecha_inicio, 'YYYY-MM-DD"T"HH24:MI:SS') resultado_fecha_inicio,
                to_char(rs.fecha_fin, 'YYYY-MM-DD"T"HH24:MI:SS') resultado_fecha_fin
            from sesion s
            left join resultado_sesion rs on (s.id = rs.id_sesion)
            order by fecha_fin desc
        """
        return db_session.execute(text(query))
