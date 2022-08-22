from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from my_tinder.models import CustomUser


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']