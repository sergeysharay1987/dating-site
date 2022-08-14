from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from my_tinder.models import CustomUser


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'gender', 'last_name']