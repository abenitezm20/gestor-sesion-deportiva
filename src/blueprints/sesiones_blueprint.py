import os
import logging
from flask import Blueprint, jsonify, make_response, request

from src.commands.sesiones.Asignar_plan import AsignarPlan


logger = logging.getLogger(__name__)
sesiones_blueprint = Blueprint('sesiones', __name__)


@sesiones_blueprint.route('/asignar_plan', methods=['POST'])
def asignar_plan():
    body = request.get_json()
    info = {
        'id_plan_deportista': body.get('id_plan_deportista', None),
        'fecha_sesion': body.get('fecha_sesion', None),
    }
    result = AsignarPlan(**info).execute()
    return make_response(jsonify({'result': result}), 200)
