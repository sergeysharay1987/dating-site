import os
from .apps import MyTinderConfig
from PIL import Image
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from my_tinder.models import CustomUser
from django.shortcuts import render, get_object_or_404, redirect
from dating_site.settings import BASE_DIR
from .forms import CreateClientForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from .my_tinder_services.put_watermark import put_watermark

app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак

# Create your views here.


def create_client(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})

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
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/create_client.html', {'form': bound_form})


def show_client(request, id):

    client: CustomUser = get_object_or_404(CustomUser, id=id)
    client_info = {'avatar': client.avatar,
                   'gender': client.gender,
                   'first_name': client.first_name,
                   'last_name': client.last_name}
    context = {'client': client_info}
    return render(request, 'my_tinder/client_page.html', context)


def login_client(request):
    if request.method == 'GET':
        return render(request, 'my_tinder/login_page.html', {'form': AuthenticationForm})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            #return redirect('show_client')
            return show_client(request, user.id)
        else:
            return render(request, 'my_tinder/login_page.html', {'form': AuthenticationForm})