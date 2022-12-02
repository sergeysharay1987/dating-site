from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from model_bakery import baker
from my_tinder.models import CustomUser
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest

file_name = 'image.png'

data = {
    'gender': 'M',
    'last_name': 'Ivanov',
    'email': 'Ivanov_1000@gmail.com',
    'password1': 'qwerty1000',
    'password2': 'qwerty1000'
}

LIST_PATH = '/my_tinder/clients/'
FILTER_PATH = '/my_tinder/clients/?first_name=Jack'
RETRIEVE_PATH = '/my_tinder/clients/'  # user id add in test_retrieve
CREATE_PATH = '/my_tinder/dj-rest-auth/registration/'
LOGIN_PATH = '/my_tinder/dj-rest-auth/login/'

REMOTE_ADDR = '199.7.2.0'
REMOTE_ADDR_KOL = '10.0.2.15'
GET_LOCATION_URL = f'http://ip-api.com/json/{REMOTE_ADDR}'


@pytest.mark.django_db
def test_list(api_client):
    api_response = api_client.get(path=LIST_PATH, format='json')
    assert api_response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=CREATE_PATH, data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


def test_retrieve(api_client, list_users):
    other_user = CustomUser.objects.get(email='jack_sparrow@gmail.com')
    other_user_id = other_user.id
    api_response = api_client.get(path=f'{RETRIEVE_PATH}{other_user_id}', format='json')
    if CustomUser.objects.contains(other_user):
        assert api_response.status_code == HTTP_200_OK
    elif not CustomUser.objects.contains(other_user):
        assert api_response.status_code == HTTP_404_NOT_FOUND


# find the way to get request.user.id to exclude it in CustomUser.objects.all()
def test_filter(api_client, list_users):
    query_params = {'first_name': 'J', 'gender': 'M'}
    api_response = api_client.get(FILTER_PATH, query_params)
    assert api_response.status_code == HTTP_200_OK
    # assert api_response.json() == CustomUser.objects.all()


@pytest.mark.django_db
def test_login():
    auth_user = CustomUser.objects.create_user(email='auth_user@gmail.com', password='appleapple')
    api_client = APIClient()
    api_response = api_client.post(
        LOGIN_PATH, data={
            'email': auth_user.email,
            'password': 'appleapple'
        }, format='json'
    )
    assert api_response.status_code == 200
    assert api_response.json()['key'] == CustomUser.objects.get(id=auth_user.id).auth_token.key


@pytest.mark.parametrize('distance', [10, 100, 1000, 10000, 100000])
def test_get_neariest_users(distance, list_users):
    user = baker.make(
        'my_tinder.CustomUser', email='auth_user@yandex.ru', first_name='auth_user', location=Point(52.2740, 4.7897)
    )

    user_point = user.location
    neariest_users = CustomUser.objects.filter(location__distance_lte=(user_point, D(km=distance))).exclude(id=user.id)
    print(f'neariest_users: {neariest_users} at distance {dir(D)}')
