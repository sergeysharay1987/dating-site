from io import BytesIO
from dating_site.settings import BASE_DIR
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client
import pytest
import json
from django.urls import reverse
from PIL import Image
from my_tinder.apps import MyTinderConfig
from my_tinder.forms import CreateClientForm
from rest_framework.test import APIClient

from my_tinder.models import CustomUser
from my_tinder.serializers import CustomUserSerializer
from rest_framework.renderers import JSONRenderer

import pytest

from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'data_for_testing.json')


data = {
    'gender': 'M',
    'last_name': 'Ivanov',
    'email': 'Ivanov_1000@gmil.com',
    'password1': 'qwerty1000',
    'password2': 'qwerty1000'}

image_path = f'/{BASE_DIR}/{MyTinderConfig.name}/tests/image.png'


def get_file_data(path: str):
    image = Image.open(path)
    bytes_io = BytesIO()
    image.save(bytes_io, 'png')
    return bytes_io.getvalue()


file_data = get_file_data(image_path)
file_data_form = {'avatar': SimpleUploadedFile('image.png', file_data,
                                               content_type=f'image/png')}


# @pytest.mark.django_db
# def test_user_creation_form():
#     bound_form = CreateClientForm(data, file_data_form)
#     if bound_form.is_valid():
#         bound_form.save()
#         users = get_user_model().objects.all()
#         assert users.count() == 1
#     else:
#         return bound_form.errors
#
#
# @pytest.mark.django_db
# def test_registration():
#     client = Client()
#     with open(image_path, 'rb') as fp:
#         resp: HttpResponse = client.post(reverse('registration'), {'avatar': fp,
#                                                                    'gender': 'M',
#                                                                    'last_name': 'Ivanov',
#                                                                    'email': 'Ivanov_1000@gmail.com',
#                                                                    'password1': 'qwerty1000',
#                                                                    'password2': 'qwerty1000'})
#
#         assert resp.status_code == 200
#         assert get_user_model().objects.get(email='Ivanov_1000@gmail.com')
#
#
# @pytest.mark.django_db
# def test_registration_invalid_data():
#     client = Client()
#     with open(image_path, 'rb') as fp:
#         resp: HttpResponse = client.post(reverse('registration'), {'avatar': fp,
#                                                                    'gender': 'M',
#                                                                    'last_name': 0,
#                                                                    'email': 'Ivanov_10001gmail.com',
#                                                                    'password1': 'qwerty1000',
#                                                                    'password2': 'qwerty1000'})
#
#         assert resp.status_code == 200
#         assert not get_user_model().objects.filter(email='Ivanov_10001gmail.com').exists()


@pytest.mark.django_db
def test_list():
    queryset = CustomUser.objects.all()
    serializer = CustomUserSerializer(queryset, many=True)
    # serializer.is_valid()
    json_queryset = JSONRenderer().render(serializer.data)
    #print(f'type(json_queryset): {type(json_queryset):}')
    #print(f'serializer.data: {type(serializer.data)}')
   # print(f'json: {json}')
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    api_response = api_client.get(path=reverse('customuser-list'), format='json')
    api_response.render()
    ser_api_response = CustomUserSerializer(data=api_response.data)
    ser_api_response.is_valid()
    print(f'ser_api_response.is_valid(): {ser_api_response.errors}')
    #print(f'ser_api_response.data: {ser_api_response.validated_data}')
    #print(f'api_response.content: {api_response.content}')
    #print(f'json_response: {json_response}')
    #print(f'json_queryset: {json_queryset}')
    #api_response.content
    assert api_response.status_code == 200
    #assert json_response == json_queryset
    assert len(api_response.content) == len(json_queryset)