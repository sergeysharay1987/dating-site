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


@pytest.fixture()
def list_users_with_coords(db):
    return [
        baker.make(
            'my_tinder.CustomUser',
            email='jack_sparrow@gmail.com',
            first_name='Jack',
            last_name='Sparrow',
            gender='М',
            location=Point(52.3740, 4.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='jack_smith@gmail.com',
            first_name='Jack',
            last_name='Smith',
            gender='М',
            location=Point(42.3740, 8.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='jack_daniels@gmail.com',
            first_name='Jack',
            last_name='Daniels',
            gender='М',
            location=Point(32.3740, 3.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='elizabeth_swon@gmail.com',
            first_name='Elizabeth',
            last_name='Swon',
            gender='Ж',
            location=Point(72.3740, 8.8897)
        ),
        baker.make(
            'my_tinder.CustomUser',
            email='tia_dalma@gmail.com',
            first_name='Tia',
            last_name='Dalma',
            gender='Ж',
            location=Point(45.3740, 4.597)
        )
    ]
