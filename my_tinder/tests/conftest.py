import pytest
from django.contrib.gis.geos import Point
from model_bakery import baker
from rest_framework.test import APIClient


@pytest.fixture()
def api_client(db):
    user = baker.make(
        'my_tinder.CustomUser', email='auth_user@yandex.ru', first_name='auth_user', location=Point(52.2740, 4.7897)
    )
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture()
def list_users():
    return [
        baker.make(
            'my_tinder.CustomUser',
            email='jack_sparrow@gmail.com',
            first_name='Jack',
            last_name='Sparrow',
            gender='M',
            location=Point(52.3740, 4.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='jack_smith@gmail.com',
            first_name='Jack',
            last_name='Smith',
            gender='M',
            location=Point(42.3740, 8.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='jack_daniels@gmail.com',
            first_name='Jack',
            last_name='Daniels',
            gender='M',
            location=Point(32.3740, 3.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='elizabeth_swon@gmail.com',
            first_name='Elizabeth',
            last_name='Swon',
            gender='F',
            location=Point(72.3740, 8.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='tia_dalma@gmail.com',
            first_name='Tia',
            last_name='Dalma',
            gender='F',
            location=Point(45.3740, 4.597)
        )
    ]
