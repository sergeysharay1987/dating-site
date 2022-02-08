from django.shortcuts import render
from .forms import CreateClientForm
# Create your views here.


def create_client(request):
    if request.method == 'GET':
        form = CreateClientForm()
        return render(request, 'my_tinder/create_client.html', {'form': form})
    elif request.method == 'POST':
        bound_form = CreateClientForm(request.POST, request.FILES)
        if bound_form.is_valid():

            data = bound_form.cleaned_data
            bound_form = CreateClientForm(data)
            bound_form.save()
            return render(request, 'my_tinder/create_client.html', {'form': bound_form})
