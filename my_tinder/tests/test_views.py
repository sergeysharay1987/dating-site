import requests
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from model_bakery import baker

from my_tinder.models import CustomUser
from my_tinder.my_tinder_services.put_watermark import get_lat_long, get_lat_long_free
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest

file_name = 'image.png'

data = {'gender': 'М', 'last_name': 'Ivanov', 'email': 'Ivanov_1000@gmail.com', 'password': 'qwerty1000'}

LIST_PATH = '/my_tinder/clients/'
FILTER_PATH = '/my_tinder/list?first_name=Jack'
RETRIEVE_PATH = '/my_tinder/clients/'  # user id add in test_retrieve
CREATE_PATH = '/my_tinder/clients/dj-rest-auth/registration/'
LOGIN_PATH = '/my_tinder/dj-rest-auth/login/'

REMOTE_ADDR = '199.7.2.0'
REMOTE_ADDR_KOL = '10.0.2.15'
GET_LOCATION_URL = f'http://ip-api.com/json/{REMOTE_ADDR}'


@pytest.mark.django_db
def test_list(api_client):
    api_response = api_client.get(path=LIST_PATH, format='json')
    assert api_response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create(api_client):
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


@pytest.mark.django_db
def test_filter(api_client, list_users):
    query_params = {'first_name': 'Jack'}
    api_response = api_client.get(FILTER_PATH, query_params)
    assert api_response.status_code == HTTP_200_OK


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


@pytest.mark.django_db
def test_get_user_ip(api_client):
    api_response = api_client.get(RETRIEVE_PATH, REMOTE_ADDR='10.0.2.15')
    assert api_response.content


def test_get_user_location():
    response = requests.get(GET_LOCATION_URL)
    print(response.content)


def test_get_lat_long():
    user_ip = get_lat_long('10.0.2.15')
    print(f'user_ip: {user_ip}')
    assert isinstance(user_ip, list)


def test_get_lat_long_free():
    user_ip = get_lat_long_free('172.19.0.1')
    print(f'user_ip: {user_ip}')


@pytest.mark.django_db
def test_remote_addr(api_client):
    api_response = api_client.get(LIST_PATH, REMOTE_ADDR=REMOTE_ADDR)
    print(api_response.request)


@pytest.mark.parametrize('distance', [10, 100, 1000, 10000, 100000])
def test_get_neariest_users(distance, list_users_with_coords):
    user = baker.make(
        'my_tinder.CustomUser', email='auth_user@yandex.ru', first_name='auth_user', location=Point(52.2740, 4.7897)
    )

    user_point = user.location
    neariest_users = CustomUser.objects.filter(location__distance_lte=(user_point, D(km=distance))).exclude(id=user.id)
    print(f'neariest_users: {neariest_users} at distance {dir(D)}')
