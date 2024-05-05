import json
import logging
import pytest
import uuid

from faker import Faker
from src.main import app
from src.models.app_externa import AppExterna, EstadoAppExternaEnum
from src.models.db import db_session
from unittest.mock import patch, MagicMock


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestServicios")

    with db_session() as session:
        email = fake.email()

        # Crear app externa
        app_externa: AppExterna = AppExterna(nombre=fake.name(),
                                             descripcion=fake.text(),
                                             estado=EstadoAppExternaEnum.activa,
                                             webhook=fake.url(),
                                             token=uuid.uuid4(),
                                             email=email)
        session.add(app_externa)
        session.commit()

        app = {
            'nombre': app_externa.nombre,
            'descripcion': app_externa.descripcion,
            'webhook': app_externa.webhook,
            'token': app_externa.token,
        }

        yield {
            'email': email,
            'app_externa': app,
        }

        session.delete(app_externa)
        session.commit()

        logger.info("Fin TestServicios")


@ pytest.mark.usefixtures("setup_data")
class TestServicios():

    @ patch('requests.post')
    def test_obtener_apps(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                '/gestor-sesion-deportiva/servicios-externo/obtener_apps', headers=headers)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert len(response_json) > 0

    @ patch('requests.post')
    def test_obtener_apps_sin_email(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': None}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            response = test_client.get(
                '/gestor-sesion-deportiva/servicios-externo/obtener_apps', headers=headers)

            assert response.status_code == 400

    @ patch('requests.post')
    def test_registrar_app(self, mock_post, setup_data: dict):
        with db_session() as session:
            with app.test_client() as test_client:
                email: str = setup_data['email']

                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    'token_valido': True, 'email': email}
                mock_post.return_value = mock_response

                headers = {'Authorization': 'Bearer 123'}
                body = {
                    'nombre': fake.name(),
                    'descripcion': fake.text(),
                    'webhook': fake.url(),
                    'token': uuid.uuid4(),
                }
                response = test_client.post(
                    '/gestor-sesion-deportiva/servicios-externo/registrar_app', headers=headers, json=body)
                response_json = json.loads(response.data)

                assert response.status_code == 200
                assert 'result' in response_json
                assert 'id' in response_json['result']
                assert 'estado' in response_json['result']

                app_creada = session.query(AppExterna).filter(
                    AppExterna.id == response_json['result']['id']).first()
                session.delete(app_creada)
                session.commit()

    @ patch('requests.post')
    def test_registrar_app_sin_email(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': None}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'nombre': fake.name(),
                'descripcion': fake.text(),
                'webhook': fake.url(),
                'token': uuid.uuid4(),
            }
            response = test_client.post(
                '/gestor-sesion-deportiva/servicios-externo/registrar_app', headers=headers, json=body)

            assert response.status_code == 400

    @patch('requests.post')
    def test_registrar_app_sin_nombre(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': setup_data['email']}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'nombre': None,
                'descripcion': fake.text(),
                'webhook': fake.url(),
                'token': uuid.uuid4(),
            }
            response = test_client.post(
                '/gestor-sesion-deportiva/servicios-externo/registrar_app', headers=headers, json=body)

            assert response.status_code == 400

    @patch('requests.post')
    def test_registrar_app_ya_registrada(self, mock_post, setup_data: dict):
        with app.test_client() as test_client:
            email: str = setup_data['email']
            app_externa = setup_data['app_externa']

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                'token_valido': True, 'email': email}
            mock_post.return_value = mock_response

            headers = {'Authorization': 'Bearer 123'}
            body = {
                'nombre': app_externa['nombre'],
                'descripcion': app_externa['descripcion'],
                'webhook': app_externa['webhook'],
                'token': app_externa['token'],
            }
            response = test_client.post(
                '/gestor-sesion-deportiva/servicios-externo/registrar_app', headers=headers, json=body)

            assert response.status_code == 400
