from io import BytesIO
# from django.shortcuts import reverse
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer

from dating_site.settings import BASE_DIR
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
# from django.urls import reverse
from PIL import Image
from my_tinder.apps import MyTinderConfig
from rest_framework.test import APIClient
from my_tinder.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest
from django.core.management import call_command

from my_tinder.my_tinder_services.put_watermark import put_watermark
from my_tinder.urls import router
from my_tinder.serializers import CustomUserSerializer
from django.db.models import F


class CustomUserSerializerTesting(ModelSerializer):
    DOMAIN = 'http://testserver'

    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']

    def save(self, **kwargs):
        if self.data.get('avatar'):
            relative_url = self.data['avatar'].url
            self.data['avatar'].url = CustomUserSerializerTesting.DOMAIN + relative_url
            print(f'self.data["avatar"].url: {self.data["avatar"].url}')
            return super().save()
        if self.validated_data.get('avatar'):
            base_image: Image = Image.open(self.validated_data['avatar'].file)
            watermarked_image: BytesIO = put_watermark(base_image)
            self.validated_data['avatar'].file = watermarked_image

        return super().save()


@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'data_for_testing.json')


file_name = 'image.png'
image_path = f'/{BASE_DIR}/{MyTinderConfig.name}/tests/{file_name}'


# def get_file_data(path: str):
#     image = Image.open(path)
#     bytes_io = BytesIO()
#     image.save(bytes_io, 'png')
#     return bytes_io.getvalue()

def get_file_data(path: str):
    image = Image.open(path)
    bytes_io = BytesIO()
    image.save(bytes_io, 'PNG')
    bytes_io.read()
    content = bytes_io.getvalue()
    return content


size = Image.open(image_path).size
file_data = get_file_data(image_path)
file_data_form = {'avatar': SimpleUploadedFile('image.png', file_data,
                                               content_type=f'image/{file_name.split(".")[-1]}')}

# data = {'avatar': InMemoryUploadedFile(name='image.png', size=size, charset=None,
#                                        content_type=f'image/{file_name.split(".")[-1]}', field_name='avatar',
#                                        file=file_data),
#         'gender': 'М',
#         'last_name': 'Ivanov',
#         'email': 'Ivanov_1000@gmil.com',
#         'password1': 'qwerty1000',
#         'password2': 'qwerty1000'}

data = {
    'gender': 'М',
    'last_name': 'Ivanov',
    'email': 'Ivanov_1000@gmail.com',
    'password1': 'qwerty1000',
    'password2': 'qwerty1000'}

queryset = CustomUser.objects.all()[:10]


@pytest.fixture(autouse=True)
def use_dummy_cache_backend(settings):
    settings.MEDIA_URL = 'http://testserver'
    settings.ALLOWED_HOSTS = ['testserver']


@pytest.fixture(params=[queryset])
def user(request):
    for user in request.param:
        print(f'user: {user}')
        return user


@pytest.mark.django_db
def test_list():
    queryset = CustomUser.objects.all().exclude(id=7)
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    api_response = api_client.get(path=reverse(router.urls[0].name), format='json')
    serializer = CustomUserSerializer(queryset, many=True)
    assert api_response.status_code == HTTP_200_OK
    assert api_response.data == serializer.data


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=reverse(router.urls[2].name), data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve(user):
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    api_response = api_client.get(path=reverse(router.urls[4].name, kwargs={'pk': 1}), format='json')
    other_user = CustomUser.objects.get(id=1)
    if CustomUser.objects.contains(other_user):

        serilaizer = CustomUserSerializer(other_user)
        assert api_response.status_code == HTTP_200_OK
        assert api_response.data == serilaizer.data
    else:

        assert api_response.status_code == HTTP_404_NOT_FOUND


# @pytest.fixture(params=[])
# def quey_params()





@pytest.mark.django_db
def test_filter():

    query_params = {'first_name': 'Jack'}
    api_client = APIClient()
    api_client.force_authenticate(CustomUser.objects.get(id=7))
    url = reverse(router.urls[0].name)
    api_response = api_client.get(url, query_params)
    serilizer = CustomUserSerializer(CustomUser.objects.filter(first_name__exact='Jack'), many=True)
    assert serilizer.data == api_response.data
