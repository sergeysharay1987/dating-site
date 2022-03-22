from PIL import Image
from my_tinder.models import CustomUser
from django.shortcuts import render
from dating_site.settings import MEDIA_ROOT
from .forms import CreateClientForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from .put_watermark import put_watermark


def create_client(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():

            image_field: InMemoryUploadedFile = bound_form.cleaned_data['avatar']
            image = Image.open(image_field, mode='r')
            watermarked_image = put_watermark(image, f'{MEDIA_ROOT}/watermark_background.png')
            watermarked_image.seek(0)
            file_data = {'avatar': SimpleUploadedFile(f'image.png', watermarked_image.read(),
                                                      content_type=f'image/png')}
            last_name = bound_form.cleaned_data['last_name']
            gender = bound_form.cleaned_data['gender']
            email = bound_form.cleaned_data['email']
            password1 = bound_form.cleaned_data['password1']
            password2 = bound_form.cleaned_data['password2']
            data = {'gender': gender,
                    'last_name': last_name,
                    'email': email,
                    'password1': password1,
                    'password2': password2}
            bound_form = CreateClientForm(data, file_data)
            bound_form.save()
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/create_client.html', {'form': bound_form})


def show_client(request, id):
    client: CustomUser = CustomUser.objects.get(id=id)

    client_info = {'avatar': client.avatar,
                   'gender': client.gender,
                   'first_name': client.first_name,
                   'last_name': client.last_name}
    context = {'client': client_info}
    return render(request, 'my_tinder/client_page.html', context)
