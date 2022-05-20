from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, ModelForm
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

        widgets = {  # 'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }


class ToLikeClientForm(ModelForm):
    like = CharField(label='', max_length=100, widget=forms.TextInput(
        attrs={'class': 'btn btn-light active', 'type': 'submit', 'value': 'Нравится'}))
    dislike = CharField(label='', max_length=100,
                        widget=forms.TextInput(
                            attrs={'class': 'btn btn-light active', 'type': 'submit', 'aria-pressed':'True', 'value': 'Не нравится'}))

    class Meta:
        model = CustomUser
        fields = ['like']

