from io import BytesIO
from django.contrib.auth import get_user_model
from rest_framework.fields import ImageField
from rest_framework.serializers import ChoiceField, ModelSerializer

from my_tinder.models import Gender
from my_tinder.my_tinder_services.put_watermark import put_watermark
from PIL import Image
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer


class CreateUserSerializer(RegisterSerializer):
    username = None
    avatar = ImageField(required=False)
    gender = ChoiceField(choices=Gender.choices)

    def custom_signup(self, request, user):
        if user.avatar:
            base_image: Image = Image.open(user.avatar)
            watermarked_image: BytesIO = put_watermark(base_image)
            user.avatar = watermarked_image

        return user


class LoginUserSerializer(LoginSerializer):
    username = None


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']
