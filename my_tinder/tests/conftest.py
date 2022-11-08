import pytest
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture()
def api_client(db):
    user = baker.make('my_tinder.CustomUser', email='auth_user@yandex.ru', first_name='auth_user')
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture()
def list_users(db):
    return [
        baker.make(
            'my_tinder.CustomUser', email='jack_sparrow@gmail.com', first_name='Jack', last_name='Sparrow', gender='М'
        ),
        baker.make(
            'my_tinder.CustomUser', email='jack_smith@gmail.com', first_name='Jack', last_name='Smith', gender='М'
        ),
        baker.make(
            'my_tinder.CustomUser', email='jack_daniels@gmail.com', first_name='Jack', last_name='Daniels', gender='М'
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='elizabeth_swon@gmail.com',
            first_name='Elizabeth',
            last_name='Swon',
            gender='Ж'
        ),
        baker.make(
            'my_tinder.CustomUser', email='tia_dalma@gmail.com', first_name='Tia', last_name='Dalma', gender='Ж'
        )
    ]
