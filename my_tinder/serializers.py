from io import BytesIO
from rest_framework.fields import CharField
from rest_framework.serializers import ChoiceField
from my_tinder.models import Gender
from PIL import Image
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from django.contrib.auth import get_user_model

from my_tinder.my_tinder_services.put_watermark import put_watermark


class CreateUserSerializer(RegisterSerializer):
    username = None
    gender = ChoiceField(choices=Gender.choices)
    first_name = CharField(required=False)

    def custom_signup(self, request, user):
        if self.validated_data.get('avatar'):
            base_image: Image = Image.open(self.validated_data.get('avatar').file)
            watermarked_image: BytesIO = put_watermark(base_image)
            self.validated_data.get('avatar').file = watermarked_image
            user.avatar = self.validated_data.get('avatar')
        user.gender = self.validated_data['gender']
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()


class LoginUserSerializer(LoginSerializer):
    username = None


class UserDetailSerializer(UserDetailsSerializer):

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']
