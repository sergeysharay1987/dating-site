from io import BytesIO

import django
from django.db.models import QuerySet
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer
from dating_site.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from PIL import Image
from my_tinder.apps import MyTinderConfig
from rest_framework.test import APIClient
from my_tinder.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest
from model_bakery import baker

file_name = 'image.png'
image_path = f'/{BASE_DIR}/{MyTinderConfig.name}/tests/{file_name}'


data = {
    'gender': 'М',
    'last_name': 'Ivanov',
    'email': 'Ivanov_1000@gmail.com',
    'password': 'qwerty1000'}

# queryset = baker.make('my_tinder.CustomUser', _quantity=10)
LIST_PATH = 'http://testserver/my_tinder/list'
RETRIEVE_PATH = 'http://testserver/my_tinder/clients/3'
CREATE_PATH = 'http://testserver/my_tinder/clients/create'




# @pytest.fixture(params=[queryset])
# def user(request):
#     for user in request.param:
#         print(f'user: {user}')
#         return user


@pytest.fixture()
def one_user(db):
    print(f'one_user: {baker.make("CustomUser")}')
    return baker.make(CustomUser)


@pytest.fixture()
def list_users(db):
    print(f'one_user: {baker.make("CustomUser")}')
    users = baker.make(CustomUser, _quantity=5)
    return users
    # for user in users:
    #     return user


# @pytest.mark.django_db
# def test_one_user(one_user):
#     #print(f'custimusers_from_baker: {}')
#     assert isinstance(one_user, CustomUser)

# @pytest.mark.django_db
# def test_list_users(list_users):
#     print(f'customusers_from_baker: {list_users}')
#     assert isinstance(list_users[0], CustomUser)
#     assert len(list_users) == 5


@pytest.mark.django_db
def test_list(one_user):
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=one_user.id))
    api_response = api_client.get(path=LIST_PATH, format='json')
    assert api_response.status_code == HTTP_200_OK
    # assert api_response.data == serializer.data
    # assert api_response.json() == serializer.data


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=CREATE_PATH, data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve(one_user):
    api_client = APIClient()
    # auth_user = CustomUser.objects.get(id=1)
    print(f'auth_user: {one_user}')
    api_client.force_authenticate(one_user)
    api_response = api_client.get(path=RETRIEVE_PATH, format='json')
    # other_user_id = not one_user.id
    # other_user = CustomUser.objects.get(id=RETRIEVE_PATH[-1])
    assert api_response.status_code == HTTP_200_OK
    # if CustomUser.objects.contains(other_user):
    #
    #     serilaizer = CustomUserSerializer(other_user)
    #     assert api_response.status_code == HTTP_200_OK
    #     assert api_response.data == serilaizer.data
    # else:
    #
    #     assert api_response.status_code == HTTP_404_NOT_FOUND

# @pytest.mark.django_db
# def test_filter():
#     query_params = {'first_name': 'Jack'}
#     api_client = APIClient()
#     api_client.force_authenticate(CustomUser.objects.get(id=7))
#     url = reverse(router.urls[0].name)
#     api_response = api_client.get(url, query_params)
#     serializer = CustomUserSerializer(CustomUser.objects.filter(first_name__exact='Jack'), many=True)
#     assert serializer.data == api_response.data
