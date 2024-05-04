import os
import logging
from flask import Blueprint, jsonify, make_response, request

from src.commands.sesiones.agendar_sesion import AgendarSesion
from src.commands.sesiones.finalizar_sesion_deportiva import FinalizarSesionDeportiva
from src.commands.sesiones.iniciar_sesion_deportiva import IniciarSesionDeportiva
from src.commands.sesiones.obtener_estadisticas_deportista import ObtenerEstadisticasDeportista
from src.commands.sesiones.obtener_sesiones_deportista import ObtenerSesionesDeportista
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


@sesiones_blueprint.route('/obtener_sesiones_deportista', methods=['GET'])
@token_required
def obtener_sesiones_deportista(usuario_token: UsuarioToken):
    info = {
        'email': usuario_token.email,
    }
    result = ObtenerSesionesDeportista(**info).execute()
    return make_response(jsonify({'result': result}), 200)


@sesiones_blueprint.route('/obtener_estadisticas_deportista', methods=['GET'])
@token_required
def obtener_estadisticas_deportista(usuario_token: UsuarioToken):
    info = {
        'email': usuario_token.email
    }
    result = ObtenerEstadisticasDeportista(**info).execute()
    return make_response(jsonify({'result': result}), 200)


@sesiones_blueprint.route('/iniciar_sesion_deportiva', methods=['POST'])
@token_required
def iniciar_sesion_deportiva(usuario_token: UsuarioToken):
    body = request.get_json()
    info = {
        'email': usuario_token.email,
        'id_sesion': body.get('id_sesion', None),
    }
    result = IniciarSesionDeportiva(**info).execute()
    return make_response(jsonify({'result': result}), 200)


@sesiones_blueprint.route('/finalizar_sesion_deportiva', methods=['POST'])
@token_required
def finalizar_sesion_deportiva(usuario_token: UsuarioToken):
    body = request.get_json()
    info = {
        'email': usuario_token.email,
        'id_sesion': body.get('id_sesion', None),
        'fecha_inicio': body.get('fecha_inicio', None),
        'fecha_fin': body.get('fecha_fin', None),
        'vo2_max': body.get('vo2_max', None),
        'ftp': body.get('ftp', None),
    }
    result = FinalizarSesionDeportiva(**info).execute()
    return make_response(jsonify({'result': result}), 200)
