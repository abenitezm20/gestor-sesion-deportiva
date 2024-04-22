import os
import logging
from flask import Blueprint, jsonify, make_response, request

from src.commands.sesiones.agendar_sesion import AgendarSesion


logger = logging.getLogger(__name__)
sesiones_blueprint = Blueprint('sesiones', __name__)


@sesiones_blueprint.route('/agendar_sesion', methods=['POST'])
def agendar_sesion():
    body = request.get_json()
    info = {
        'id_plan_deportista': body.get('id_plan_deportista', None),
        'fecha_sesion': body.get('fecha_sesion', None),
    }
    result = AgendarSesion(**info).execute()
    return make_response(jsonify({'result': result}), 200)
