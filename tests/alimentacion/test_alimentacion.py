import json
import pytest
import logging
import uuid
from unittest.mock import patch, MagicMock

from faker import Faker
from src.main import app
from src.models.db import db_session
from src.models.menu import Menu
from src.models.plan_alimenticio import PlanAlimenticio
from src.models.tipo_plan_alimenticio import TipoPlanAlimenticio


fake = Faker()
logger = logging.getLogger(__name__)


@pytest.fixture(scope="class")
def setup_data():
    logger.info("Inicio TestAlimentacion")

    # Crear menu
    menu = {
        'nombre': fake.word(),
        'calorias': fake.random_int(min=0, max=500),
        'porcion': fake.random_int(min=0, max=500),
        'medida': 'g',
        'descripcion': fake.name()
    }
    menu_random: Menu = Menu(**menu)
    logger.info('Menu creado: ' + str(menu))
    db_session.add(menu_random)
    db_session.commit()

    # Crear tipo plan alimenticio
    tipo_plan = {
        'nombre': fake.word(),
    }
    tipo_plan_random: TipoPlanAlimenticio = TipoPlanAlimenticio(**tipo_plan)
    logger.info('Tipo plan alimenticio creado: ' + str(tipo_plan))
    db_session.add(tipo_plan_random)
    db_session.commit()

    # Crear plan alimenticio
    plan_alimenticio = {
        'id_tipo_plan_alimenticio': tipo_plan_random.id,
        'id_menu': menu_random.id,
        'id_plan': str(uuid.uuid4())
    }
    plan_alimenticio_random = PlanAlimenticio(**plan_alimenticio)
    logger.info('Plan alimenticio creado: ' + str(plan_alimenticio))
    db_session.add(plan_alimenticio_random)
    db_session.commit()

    yield {
        'menu': menu_random,
        'tipo_plan': tipo_plan_random,
        'plan_alimenticio': plan_alimenticio_random
    }

    logger.info("Fin TestAlimentacion")
    db_session.delete(plan_alimenticio_random)
    db_session.delete(tipo_plan_random)
    db_session.delete(menu_random)
    db_session.commit()


@pytest.mark.usefixtures("setup_data")
class TestAlimentacion():

    def test_obtener_plan(self, setup_data: dict):
        with app.test_client() as test_client:
            id_plan = setup_data['plan_alimenticio'].id_plan

            body = {
                "id_plan": id_plan
            }

            response = test_client.post(
                '/gestor-plan-alimenticio/alimentacion/obtener_plan', json=body)
            response_json = json.loads(response.data)

            assert response.status_code == 200
            assert 'result' in response_json
            assert len(response_json['result']) > 0
