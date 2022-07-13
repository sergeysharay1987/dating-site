from io import BytesIO
from dating_site.settings import BASE_DIR
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client
import pytest
from django.urls import reverse
from PIL import Image
from my_tinder.apps import MyTinderConfig
from my_tinder.forms import CreateClientForm

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


@pytest.mark.django_db
def test_user_creation_form():
    print(image_path)
    bound_form = CreateClientForm(data, file_data_form)
    if bound_form.is_valid():
        bound_form.save()
        users = get_user_model().objects.all()
        assert users.count() == 1
    else:
        return bound_form.errors


@pytest.mark.django_db
def test_registration():
    client = Client()
    with open(image_path, 'rb') as fp:
        resp: HttpResponse = client.post(reverse('registration'), {'avatar': fp,
                                                                   'gender': 'M',
                                                                   'last_name': 'Ivanov',
                                                                   'email': 'Ivanov_1000@gmail.com',
                                                                   'password1': 'qwerty1000',
                                                                   'password2': 'qwerty1000'})
        if resp.status_code != 200:
            print(f'response: {resp.content}')

        assert get_user_model().objects.get(email='Ivanov_1000@gmail.com')


img = BytesIO(file_data)
img.name = 'image.png'

'''@pytest.mark.django_db
def test_registration():
    client = Client()
    resp: HttpResponse = client.post(reverse('registration'), {'avatar': img,
                                                               'gender': 'M',
                                                               'last_name': 'Ivanov',
                                                               'email': 'Ivanov_1000@gmail.com',
                                                               'password1': 'qwerty1000',
                                                               'password2': 'qwerty1000'}
                                     )
    assert get_user_model().objects.get(email='Ivanov_1000@gmail.com')'''
