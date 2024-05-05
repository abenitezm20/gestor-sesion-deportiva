import logging

from flask import Blueprint, jsonify, make_response, request
from src.commands.servicios.obtener_apps import ObtenerApps
from src.commands.servicios.registrar_app import RegistrarApp
from src.utils.seguridad_utils import UsuarioToken, token_required


logger = logging.getLogger(__name__)
servicios_externo_blueprint = Blueprint('servicios-externo', __name__)


@servicios_externo_blueprint.route('/obtener_apps', methods=['GET'])
@token_required
def obtener_apps(usuario_token: UsuarioToken):
    info = {
        'email': usuario_token.email,
    }
    result = ObtenerApps(**info).execute()
    return make_response(jsonify({'result': result}), 200)


@servicios_externo_blueprint.route('/registrar_app', methods=['POST'])
@token_required
def registrar_app(usuario_token: UsuarioToken):
    body = request.get_json()
    info = {
        'email': usuario_token.email,
        'nombre': body.get('nombre'),
        'descripcion': body.get('descripcion'),
        'webhook': body.get('webhook'),
        'token': body.get('token'),
    }
    result = RegistrarApp(**info).execute()
    return make_response(jsonify({'result': result}), 200)
