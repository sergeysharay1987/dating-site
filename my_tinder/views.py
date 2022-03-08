from PIL import Image
from PIL.ImageFile import ImageFile
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
            #print(f'request.FILES: {request.FILES["avatar"]}')
            #print(f'dir(request.FILES["avatar"]): {dir(request.FILES["avatar"])}')
            #if request.FILES:
            image_field: InMemoryUploadedFile = bound_form.cleaned_data['avatar']
            print(f'type(image_field):{type(image_field)}')
            #print(f'{image_field.image}')
            print(f'image_field.file: {image_field.file}')
            print(f'type(image_field): {type(image_field)}')

            image = Image.open(image_field, mode='r')
            print(f'image_location: {image.format}')
            print(f'image: {image}')

            watermarked_image: ImageFile = put_watermark(image, f'{MEDIA_ROOT}/watermark.jpg')

            watermarked_image.show()
            print(f'type_of_watermark_image: {watermarked_image.filename}')
            last_name = bound_form.cleaned_data['last_name']
            gender = bound_form.cleaned_data['gender']
            email = bound_form.cleaned_data['email']
            password1 = bound_form.cleaned_data['password1']
            password2 = bound_form.cleaned_data['password2']
            #bound_form.cleaned_data["avatar"].image = watermarked_image
            #bound_form.cleaned_data["avatar"].image.show()
            data = {'gender': gender, 'last_name': last_name, 'email': email, 'password1':password1, 'password2': password2}
            extension:str = watermarked_image.format.lower()
            watermarked_image.save()
            if extension == 'jpeg':
                extension = 'jpg'

            print(f'type(watermarked_image): {type(watermarked_image)}')
            #file_data = {'avatar': SimpleUploadedFile(f'image.{extension}', watermarked_image.tobytes(), content_type=f'image/{extension}')}
            file_data = {'avatar': SimpleUploadedFile(f'image.png', watermarked_image.tobytes(),
                                                      content_type=f'image/png')}
            print(f'file_data["avatar"].size: {file_data["avatar"].size}')
            print(f'file_data: {file_data}')
            bound_form = CreateClientForm(data, file_data)
            bound_form.is_valid()
            print(f'bound_form.errors: {bound_form.errors}')
            bound_form.save()
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
