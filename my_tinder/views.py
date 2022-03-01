from django.shortcuts import render

from dating_site.settings import MEDIA_ROOT
from .forms import CreateClientForm


# Create your views here.
from .put_watermark import put_watermark


def create_client(request):
    if request.method == 'GET':

        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})

    elif request.method == 'POST':

        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():
            print(request.FILES)
            if request.FILES:
                request.FILES['avatar'] = put_watermark(request.FILES['avatar'], f'{MEDIA_ROOT}/watermark.jpg')
            data = bound_form.cleaned_data
            bound_form = CreateClientForm(data, request.FILES)
            bound_form.save()
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
        else:

            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
