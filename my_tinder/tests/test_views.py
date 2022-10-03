from io import BytesIO
from dating_site.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from PIL import Image
from my_tinder.apps import MyTinderConfig
from rest_framework.test import APIClient
from my_tinder.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest
from django.core.management import call_command
from my_tinder.urls import router


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'data_for_testing.json')


data = {
    'gender': 'М',
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


@pytest.fixture(params=[[1, 2, 3]])  # /calculator/
@pytest.mark.django_db
def get_user(request):
    print(f'request.param: {request.param}')
    # for user in request.param:
    #     yield user
    return CustomUser.objects.get(request.param)
    # return request.param


@pytest.mark.django_db
def test_print_user(get_user):
    print(f'get_user: {get_user}')
    return get_user


@pytest.mark.django_db
def test_list():
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    api_response = api_client.get(path=reverse(router.urls[0].name), format='json')
    api_response.render()
    assert api_response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=reverse(router.urls[2].name), data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve(get_user):
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    api_response = api_client.get(path=reverse(router.urls[4].name, kwargs={'pk': get_user.pk}), format='json')
    if CustomUser.objects.contains(get_user):
        assert api_response.status_code == HTTP_200_OK
    else:
        assert api_response.status_code == HTTP_404_NOT_FOUND
