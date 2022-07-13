import os
from io import BytesIO
from dating_site.settings import BASE_DIR
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client
# Create your tests here.
import pytest
from django.urls import reverse
from PIL import Image

from dating_site import settings
from my_tinder.apps import MyTinderConfig
from my_tinder.forms import CreateClientForm

# im = Image.open('image.png')
# byte_io = BytesIO()
# byte_io.seek(0)
# im.save(byte_io, 'PNG')

#
# @pytest.fixture(scope='session')
# def django_db_setup():
#     settings.DATABASES['test_db'] = {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }

data = {
    'gender': 'M',
    'last_name': 'Ivanov',
    'email': 'Ivanov_1000@gmil.com',
    'password1': 'qwerty1000',
    'password2': 'qwerty1000'}

# path = f'/dating_site/my_tinder/tests/image.png'
path = f'/{BASE_DIR}/{MyTinderConfig.name}/tests/image.png'


def get_file_data(path: str):
    image = Image.open(path)
    bytes_io = BytesIO()
    image.save(bytes_io, 'png')
    #print(f'cwd: {os.getcwd()}')

    return bytes_io.getvalue()


file_data = get_file_data(path)
file_data = {'avatar': SimpleUploadedFile('image.png', file_data,
                                          content_type=f'image/png')}


'''@pytest.mark.django_db
def test_user_creation_form():
    print(path)
    bound_form = CreateClientForm(data, file_data)
    if bound_form.is_valid():
        bound_form.save()
    else:
        return 0
    users = get_user_model().objects.all()
    assert users.count() == 1'''


@pytest.mark.django_db
def test_registration():
    client = Client()
    with open(path, 'rb') as fp:
        resp: HttpResponse = client.post(reverse('registration'), {'avatar': fp,
                                                               'gender': 'M',
                                                               'last_name': 'Ivanov',
                                                               'email': 'Ivanov_1000@gmail.com',
                                                               'password1': 'qwerty1000',
                                                               'password2': 'qwerty1000'}
                                     )
    assert get_user_model().objects.get(email='Ivanov_1000@gmail.com')

