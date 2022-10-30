from rest_framework.test import APIClient
from my_tinder.models import CustomUser
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
import pytest
from model_bakery import baker

file_name = 'image.png'

data = {'gender': 'М', 'last_name': 'Ivanov', 'email': 'Ivanov_1000@gmail.com', 'password': 'qwerty1000'}

# queryset = baker.make('my_tinder.CustomUser', _quantity=10)
LIST_PATH = 'http://testserver/my_tinder/list'
FILTER_PATH = 'http://testserver/my_tinder/list?first_name=Jack'
RETRIEVE_PATH = 'http://testserver/my_tinder/clients/1'
CREATE_PATH = 'http://testserver/my_tinder/clients/create'

# @pytest.fixture(params=[queryset])
# def user(request):
#     for user in request.param:
#         print(f'user: {user}')
#         return user


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        baker.make('my_tinder.CustomUser', _quantity=5)


@pytest.fixture()
def api_client(db):
    user = baker.make(CustomUser)
    api_client = APIClient()
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture()
def one_user():
    print(f'one_user_from_fixture_one_user: {baker.make("CustomUser")}')
    return baker.make(CustomUser)


@pytest.mark.django_db
def test_list(api_client):
    api_response = api_client.get(path=LIST_PATH, format='json')
    assert api_response.status_code == HTTP_200_OK
    # assert api_response.data == serializer.data
    # assert api_response.json() == serializer.data


@pytest.mark.django_db
def test_create():
    api_client = APIClient()
    api_response = api_client.post(path=CREATE_PATH, data=data, format='json')
    assert api_response.status_code == HTTP_201_CREATED


def test_retrieve(api_client):

    api_response = api_client.get(path=RETRIEVE_PATH, format='json')
    other_user = CustomUser.objects.get(id=RETRIEVE_PATH[-1])
    if CustomUser.objects.contains(other_user):
        assert api_response.status_code == HTTP_200_OK
    elif not CustomUser.objects.contains(other_user):
        assert api_response.status_code == HTTP_404_NOT_FOUND
    # if CustomUser.objects.contains(other_user):
    #
    #     serilaizer = CustomUserSerializer(other_user)
    #     assert api_response.status_code == HTTP_200_OK
    #     assert api_response.data == serilaizer.data
    # else:
    #
    #     assert api_response.status_code == HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_filter(api_client):
    query_params = {'first_name': 'Jack'}
    api_response = api_client.get(FILTER_PATH, query_params)
    assert api_response.status_code == HTTP_200_OK
