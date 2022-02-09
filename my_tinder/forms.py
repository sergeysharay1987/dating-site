from django.contrib.auth.forms import UserCreationForm
from .models import Client


class CreateClientForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ['avatar', 'gender', 'first_name', 'last_name', 'email']
