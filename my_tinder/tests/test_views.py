from my_tinder.models import CustomUser
from rest_framework.test import APIClient
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest

file_name = 'image.png'

data = {'gender': 'М', 'last_name': 'Ivanov', 'email': 'Ivanov_1000@gmail.com', 'password': 'qwerty1000'}

LIST_PATH = 'http://testserver/my_tinder/list'
FILTER_PATH = 'http://testserver/my_tinder/list?first_name=Jack'
RETRIEVE_PATH = 'http://testserver/my_tinder/clients/'  # user id add in test_retrieve
CREATE_PATH = 'http://testserver/my_tinder/clients/create'
LOGIN_PATH = 'http://testserver/my_tinder/dj-rest-auth/login/'


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
