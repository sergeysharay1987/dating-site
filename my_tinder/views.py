from PIL import Image
from my_tinder.models import CustomUser
from django.shortcuts import render
from dating_site.settings import MEDIA_ROOT
from .forms import CreateClientForm
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from .my_tinder_services.put_watermark import put_watermark


# Create your views here.


def create_client(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():

            data = bound_form.cleaned_data
            bound_form = CreateClientForm(data, request.FILES)
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
