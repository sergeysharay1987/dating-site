from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from dating_site.settings import BASE_DIR
from django.db.models import QuerySet
from .apps import MyTinderConfig
from PIL import Image
from my_tinder.models import CustomUser
from .forms import CreateClientForm
from .my_tinder_services.put_watermark import put_watermark

app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак

menu = [{'title': 'Зарегистрироваться', 'url_name': 'registration'},
        {'title': 'Войти', 'url_name': 'login'}]


def index(request):
    context = {'menu': menu}
    return render(request, 'my_tinder/index.html', context=context)


def registration(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/registration.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():

            image_field: InMemoryUploadedFile = bound_form.cleaned_data['avatar']
            image = Image.open(image_field, mode='r')
            watermarked_image = put_watermark(image, path_to_watermark)
            watermarked_image.seek(0)
            file_data = {'avatar': SimpleUploadedFile(f'image.png', watermarked_image.read(),
                                                      content_type=f'image/png')}
            data = bound_form.cleaned_data
            bound_form = CreateClientForm(data, file_data)
            bound_form.save()
            return render(request, 'my_tinder/registration.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/registration.html', {'form': bound_form})


@login_required()
def client_page(request, id):
    client: CustomUser = get_object_or_404(CustomUser, id=id)
    if id == request.user.id:

        client_info = {'avatar': client.avatar,
                       'gender': client.gender,
                       'first_name': client.first_name,
                       'last_name': client.last_name}
        context = {'client_info': client_info,
                   'client_email': client.email,
                   'client': client}
        return render(request, 'my_tinder/client_page.html', context)
    else:
        return redirect('client_page', id=request.user.id)


def login_client(request):
    if request.method == 'GET':
        bound_form = AuthenticationForm()
        return render(request, 'my_tinder/login_page.html', {'form': bound_form})
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        data = {'username': username, 'password': password}
        bound_form = AuthenticationForm(request, data)
        if bound_form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправление на страницу участника
                return redirect('client_page', id=request.user.id)
        else:

            return render(request, 'my_tinder/login_page.html', {'form': bound_form})


def logout_client(request):
    logout(request)
    return redirect('login', permanent=True)


@login_required()
def clients_page(request, id):
    if request.method == 'GET':
        if id == request.user.id:

            clients: QuerySet = CustomUser.objects.all()
            context = {'id': id,
                        'clients': clients}
            return render(request, 'my_tinder/clients_page.html', context=context)
        else:
            return redirect('watch_clients', id=request.user.id)


# Вьюха для просмотра подробной информации о другом участнике
@login_required()
def other_client_page(request, id, other_client_id):
    if id == request.user.id:

        other_client = get_object_or_404(CustomUser, id=other_client_id)
        other_client_info = {'avatar': other_client.avatar,
                             'gender': other_client.gender,
                             'first_name': other_client.first_name,
                             'last_name': other_client.last_name,
                             'like': other_client.like}

        context = {'id': id,
                   'other_client_id': other_client.id,
                   'other_client_info': other_client_info,
                   'other_client_email': other_client.email,
                   'other_client': other_client}

        return render(request, 'my_tinder/other_client_page.html', context)
    else:
        return redirect('other_client_detail', id=request.user.id, other_client_id=other_client_id)
