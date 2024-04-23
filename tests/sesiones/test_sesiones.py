import json
import pytest
import logging
import uuid
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.resultado_sesion import ResultadoSesion
from src.models.sesion import EstadoSesionEnum, Sesion


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestSesiones")

    # Crear sesion
    info = {
        'id_plan_deportista': uuid.uuid4(),
        'email': fake.email(),
        'estado': EstadoSesionEnum.agendada,
        'fecha_sesion': '2024-03-22T12:00:00'
    }

    sesion: Sesion = Sesion(**info)
    db_session.add(sesion)
    db_session.commit()

    # Crear resultado sesion
    info_res = {
        'id_sesion': sesion.id,
        'vo2_max': 47,
        'ftp': 2.5,
        'fecha_inicio': '2024-03-22T12:00:00',
        'fecha_fin': '2024-03-22T12:30:00'
    }
    resultado_sesion: ResultadoSesion = ResultadoSesion(**info_res)
    db_session.add(resultado_sesion)
    db_session.commit()

    yield {
        'sesion': sesion,
        'resultado_sesion': resultado_sesion
    }

    db_session.delete(resultado_sesion)
    db_session.delete(sesion)
    db_session.commit()

    logger.info("Fin TestSesiones")


@pytest.mark.usefixtures("setup_data")
class TestSesiones():

    @patch('requests.post')
    def test_obtener_sesiones_deportista(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            sesion: Sesion = setup_data['sesion']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': sesion.email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/obtener_sesiones_deportista', headers=headers, json={})
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0

    @patch('requests.post')
    def test_obtener_sesiones_deportista_fecha(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            sesion: Sesion = setup_data['sesion']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': sesion.email}
            mock_post.return_value = mock_response

            req = {
                'fecha': sesion.fecha_sesion.strftime("%Y-%m-%dT%H:%M:%S")
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/obtener_sesiones_deportista', headers=headers, json=req)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0
