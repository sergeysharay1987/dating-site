from io import BytesIO
from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer
from my_tinder.my_tinder_services.put_watermark import put_watermark
from PIL import Image


class CreateUserSerializer(ModelSerializer):
    gender = CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name', 'password']

    def save(self, **kwargs):
        if self.validated_data.get('avatar'):
            base_image: Image = Image.open(self.validated_data['avatar'].file)
            watermarked_image: BytesIO = put_watermark(base_image)
            self.validated_data['avatar'].file = watermarked_image

        return super().save(**kwargs)


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']
