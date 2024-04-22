import datetime
import logging

from sqlalchemy import func
from datetime import datetime
from src.commands.base_command import BaseCommand
from src.errors.errors import BadRequest, SesionYaAgendada
from src.models.db import db_session
from src.models.sesion import EstadoSesionEnum, Sesion
from src.utils.str_utils import str_none_or_empty


logger = logging.getLogger(__name__)


class AgendarSesion(BaseCommand):
    def __init__(self, **info):

        if str_none_or_empty(info.get('id_plan_deportista')):
            logger.error("ID Plan deportista es obligatorio")
            raise BadRequest

        if str_none_or_empty(info.get('fecha_sesion')):
            logger.error("Fecha sesion es obligatoria")
            raise BadRequest

        self.id_plan_deportista = info.get('id_plan_deportista')
        self.fecha_sesion = info.get('fecha_sesion')

    def execute(self):
        logger.info(
            f"Agendando sesion, plan deportista: {self.id_plan_deportista}, fecha: {self.fecha_sesion}")

        # Validacion que no exista una sesion ya agendada para el mismo dia
        fecha_actual = datetime.now().date()
        sesiones = db_session.query(Sesion).filter(
            Sesion.id_plan_deportista == self.id_plan_deportista,
            Sesion.estado == EstadoSesionEnum.agendada.value,
            func.DATE(Sesion.fecha_sesion) == fecha_actual).all()
        if sesiones:
            logger.error(
                f"Ya existe una sesion agendada para el dia {fecha_actual}")
            raise SesionYaAgendada

        sesion: Sesion = Sesion(
            id_plan_deportista=self.id_plan_deportista,
            fecha_sesion=self.fecha_sesion,
            estado=EstadoSesionEnum.agendada)

        db_session.add(sesion)
        db_session.commit()
        logger.info(f'Sesion asignada {sesion.id}')

        resp = {
            'id': str(sesion.id),
            'fecha_sesion': self.fecha_sesion
        }

        return resp
