import os
import logging
from flask import Blueprint, jsonify, make_response, request

from src.commands.sesiones.agendar_sesion import AgendarSesion
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
sesiones_blueprint = Blueprint('sesiones', __name__)


@sesiones_blueprint.route('/agendar_sesion', methods=['POST'])
@token_required
def agendar_sesion(usuario_token: UsuarioToken):
    body = request.get_json()
    info = {
        'id_plan_deportista': body.get('id_plan_deportista', None),
        'fecha_sesion': body.get('fecha_sesion', None),
    }
    result = AgendarSesion(usuario_token, **info).execute()
    return make_response(jsonify({'result': result}), 200)
