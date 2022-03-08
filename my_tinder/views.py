from PIL import Image
from django.shortcuts import render

from dating_site.settings import MEDIA_ROOT
from .forms import CreateClientForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

# Create your views here.
from .put_watermark import put_watermark


def create_client(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():
            #print(request.FILES)
            #if request.FILES:
            image_field: InMemoryUploadedFile = bound_form.cleaned_data['avatar']
            print(f'image_field.file: {image_field.file}')
            print(f'type(image_field): {type(image_field)}')

            image = Image.open(image_field, mode='r')
            print(f'image_location: {image.format}')
            print(f'image: {image}')
            #print(f'image_field: {image_field}')
            #watermarked_image = put_watermark(image_field, f'{MEDIA_ROOT}/watermark.jpg')
            watermarked_image = put_watermark(image, f'{MEDIA_ROOT}/watermark.jpg')
            last_name = bound_form.cleaned_data['last_name']
            gender = bound_form.cleaned_data['gender']
            email = bound_form.cleaned_data['email']
            password1 = bound_form.cleaned_data['password1']
            password2 = bound_form.cleaned_data['password2']
            data = {'gender': gender, 'last_name': last_name, 'email': email, 'password1':password1, 'password2': password2}

            file_data = {'avatar': SimpleUploadedFile(watermarked_image, watermarked_image.read())}
            print(f'watermarked_image{watermarked_image}')
            bound_form = CreateClientForm(data, file_data)
            bound_form.save()
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
