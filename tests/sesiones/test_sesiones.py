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
            response = test_client.get(
                '/gestor-sesion-deportiva/sesiones/obtener_sesiones_deportista', headers=headers)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0

    @patch('requests.post')
    def test_agendar_sesion(self, mock_post):
        with app.test_client() as test_client:
            email = fake.email()

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            req = {
                'id_plan_deportista': str(uuid.uuid4()),
                'fecha_sesion': '2024-03-22T12:00:00'
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/agendar_sesion', headers=headers, json=req)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'result' in response_json
            assert 'id' in response_json['result']
            assert 'fecha_sesion' in response_json['result']

            sesion = db_session.query(Sesion).filter(
                Sesion.id == response_json['result']['id']).first()
            db_session.delete(sesion)
            db_session.commit()

    @patch('requests.post')
    def test_obtener_estadisticas(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            sesion: Sesion = setup_data['sesion']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': sesion.email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                '/gestor-sesion-deportiva/sesiones/obtener_estadisticas_deportista', headers=headers)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'result' in response_json
            assert 'ftp' in response_json['result']
            assert 'vo2' in response_json['result']
            assert len(response_json['result']['ftp']) > 0
            assert len(response_json['result']['vo2']) > 0
