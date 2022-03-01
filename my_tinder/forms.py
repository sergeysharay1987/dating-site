from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField
from django import forms
from .models import CustomUser


class CreateClientForm(UserCreationForm):
    password1 = CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['avatar',
                  'gender',
                  'last_name',
                  'email',
                  'password1',
                  'password2']

        widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
                   'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.TextInput(attrs={'class': 'form-control'})
                   }
