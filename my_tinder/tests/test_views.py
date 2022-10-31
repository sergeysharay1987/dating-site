from rest_framework.test import APIClient
from my_tinder.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest
from model_bakery import baker

file_name = 'image.png'

data = {'gender': 'М', 'last_name': 'Ivanov', 'email': 'Ivanov_1000@gmail.com', 'password': 'qwerty1000'}

LIST_PATH = 'http://testserver/my_tinder/list'
FILTER_PATH = 'http://testserver/my_tinder/list?first_name=Jack'
RETRIEVE_PATH = 'http://testserver/my_tinder/clients/1'
CREATE_PATH = 'http://testserver/my_tinder/clients/create'


@pytest.fixture()
def api_client(db):
    user = baker.make('my_tinder.CustomUser', email='auth_user@yandex.ru', first_name='auth_user')
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture()
def list_users(db):
    baker.make(
        'my_tinder.CustomUser', email='jack_sparrow@gmail.com', first_name='Jack', last_name='Sparrow', gender='М'
    )
    baker.make('my_tinder.CustomUser', email='jack_smith@gmail.com', first_name='Jack', last_name='Smith', gender='М')
    baker.make(
        'my_tinder.CustomUser', email='jack_daniels@gmail.com', first_name='Jack', last_name='Daniels', gender='М'
    )
    baker.make(
        'my_tinder.CustomUser', email='elizabeth_swon@gmail.com', first_name='Elizabeth', last_name='Swon', gender='Ж'
    )
    baker.make('my_tinder.CustomUser', email='tia_dalma@gmail.com', first_name='Tia', last_name='Dalma', gender='Ж')
    return CustomUser.objects.all()


@pytest.mark.django_db
def test_list(api_client, list_users):
    api_response = api_client.get(path=LIST_PATH, format='json')
    assert api_response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=CREATE_PATH, data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


def test_retrieve(api_client, list_users):
    api_response = api_client.get(path=RETRIEVE_PATH, format='json')
    other_user = CustomUser.objects.get(id=RETRIEVE_PATH[-1])
    if CustomUser.objects.contains(other_user):
        assert api_response.status_code == HTTP_200_OK
    elif not CustomUser.objects.contains(other_user) or CustomUser.DoesNotExist:
        assert api_response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_filter(api_client, list_users):
    query_params = {'first_name': 'Jack'}
    api_response = api_client.get(FILTER_PATH, query_params)
    assert api_response.status_code == HTTP_200_OK
