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

    with db_session() as session:
        # Crear sesion
        info = {
            'id_plan_deportista': uuid.uuid4(),
            'email': fake.email(),
            'estado': EstadoSesionEnum.agendada,
            'fecha_sesion': '2024-03-22T12:00:00'
        }

        random_sesion: Sesion = Sesion(**info)
        session.add(random_sesion)
        session.commit()

        # Crear resultado sesion
        info_res = {
            'id_sesion': random_sesion.id,
            'vo2_max': 47,
            'ftp': 2.5,
            'fecha_inicio': '2024-03-22T12:00:00',
            'fecha_fin': '2024-03-22T12:30:00'
        }
        resultado_sesion: ResultadoSesion = ResultadoSesion(**info_res)
        session.add(resultado_sesion)
        session.commit()

        # sesion para pruebas de iniciar y finalizar
        info_sesion_prueba = {
            'id_plan_deportista': uuid.uuid4(),
            'email': random_sesion.email,
            'estado': EstadoSesionEnum.agendada,
            'fecha_sesion': '2024-05-04T12:00:00'
        }
        sesion_prueba: Sesion = Sesion(**info_sesion_prueba)
        session.add(sesion_prueba)
        session.commit()

        yield {
            'email': random_sesion.email,
            'resultado_sesion': resultado_sesion,
            'id_sesion_prueba': sesion_prueba.id,
        }

        session.delete(resultado_sesion)
        session.delete(random_sesion)
        session.delete(sesion_prueba)
        session.commit()

        logger.info("Fin TestSesiones")


@pytest.mark.usefixtures("setup_data")
class TestSesiones():

    @patch('requests.post')
    def test_obtener_sesiones_deportista(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                '/gestor-sesion-deportiva/sesiones/obtener_sesiones_deportista', headers=headers)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0

    @patch('requests.post')
    def test_agendar_sesion(self, mock_post):
        with db_session() as session:
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

                sesion = session.query(Sesion).filter(
                    Sesion.id == response_json['result']['id']).first()
                session.delete(sesion)
                session.commit()

    @patch('requests.post')
    def test_obtener_estadisticas(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
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

    @patch('requests.post')
    def test_iniciar_sesion_no_registrada(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            req = {
                'id_sesion': uuid.uuid4()
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/iniciar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_iniciar_sesion_sin_id(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            req = {
                'id_sesion': None
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/iniciar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_iniciar_sesion_exitoso(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/iniciar_sesion_deportiva', headers=headers, json=req)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'result' in response_json
            assert 'estado' in response_json['result']
            assert 'id_sesion' in response_json['result']

    @patch('requests.post')
    def test_finalizar_sesion_sin_id(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            req = {
                'id_sesion': None
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_finalizar_sesion_sin_vo2(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba,
                'ftp': 2.5,
                'fecha_inicio': '2024-05-04T12:00:00',
                'fecha_fin': '2024-05-04T12:30:00'
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_finalizar_sesion_sin_ftp(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba,
                'vo2_max': 47,
                'fecha_inicio': '2024-05-04T12:00:00',
                'fecha_fin': '2024-05-04T12:30:00'
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_finalizar_sesion_sin_fecha_inicio(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba,
                'vo2_max': 47,
                'ftp': 2.5,
                'fecha_fin': '2024-05-04T12:30:00'
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_finalizar_sesion_sin_fecha_fin(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba,
                'vo2_max': 47,
                'ftp': 2.5,
                'fecha_inicio': '2024-05-04T12:00:00',
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)

            assert response.status_code == 400

    @patch('requests.post')
    def test_finalizar_sesion_exitoso(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            id_sesion_prueba: str = setup_data['id_sesion_prueba']

            req = {
                'id_sesion': id_sesion_prueba,
                'vo2_max': 47,
                'ftp': 2.5,
                'fecha_inicio': '2024-05-04T12:00:00',
                'fecha_fin': '2024-05-04T12:30:00'
            }

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.post(
                '/gestor-sesion-deportiva/sesiones/finalizar_sesion_deportiva', headers=headers, json=req)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'result' in response_json
            assert 'estado' in response_json['result']
            assert 'id_sesion' in response_json['result']

            with db_session() as session:
                resultado_sesion = session.query(ResultadoSesion).filter(
                    ResultadoSesion.id_sesion == id_sesion_prueba).first()

                session.delete(resultado_sesion)
                session.commit()
