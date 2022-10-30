from io import BytesIO
from rest_framework.serializers import ModelSerializer
from my_tinder.models import CustomUser
from my_tinder.my_tinder_services.put_watermark import put_watermark
from PIL import Image


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']

    def save(self, **kwargs):
        if self.validated_data.get('avatar'):
            base_image: Image = Image.open(self.validated_data['avatar'].file)
            watermarked_image: BytesIO = put_watermark(base_image)
            self.validated_data['avatar'].file = watermarked_image
        return super().save()
