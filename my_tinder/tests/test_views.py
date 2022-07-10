import os
from io import BytesIO

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.test import Client
# Create your tests here.
import pytest
from django.urls import reverse
from PIL import Image

from dating_site import settings
from dating_site.settings import BASE_DIR
from my_tinder.forms import CreateClientForm

im = Image.open('image.png')
byte_io = BytesIO()
byte_io.seek(0)
im.save(byte_io, 'PNG')

file_data = {'avatar': SimpleUploadedFile('image.png', byte_io.read(),
                                          content_type=f'image/png')}
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


@pytest.mark.django_db
def test_user_creation_form():
    bound_form = CreateClientForm(data, file_data)
    print(f'byte_io: {byte_io.read()}')
    if bound_form.is_valid():
        bound_form.save()
    else:
        print(f'file_data: {file_data}')
        print(f'bound_form: {bound_form.errors}')
        return 0
    users = get_user_model().objects.all()
    assert users.count() == 1


@pytest.mark.django_db
def test_registration():
    client = Client()
    resp: HttpResponse = client.post(reverse('registration'), {'avatar': im,
                                                               'gender': 'M',
                                                               'last_name': 'Ivanov',
                                                               'email': 'Ivanov_1000@gmil.com',
                                                               'password1': 'qwerty1000',
                                                               'password2': 'qwerty1000'}
                                     )
    # print(f'response: {resp}')
    # print(f'registration_url: {reverse("registration")}')
    # queryset = CustomUser.objects.get(last_name = 'Ivanov_1000')
    # assert CustomUser.objects.get(last_name='Ivanov_1')
    bound_form = CreateClientForm(resp.reques)
    users = get_user_model().objects.all()
    print(get_user_model().objects.all())
    assert users.count() == 1
    # print(get_user_model().objects.all())
