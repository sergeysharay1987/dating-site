from PIL import Image
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from my_tinder.models import CustomUser
from my_tinder.my_tinder_services.put_watermark import put_watermark
from django.core.files import File
from PIL import Image


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['avatar', 'email', 'gender', 'first_name', 'last_name']

    def save(self, **kwargs):
        self.instance = super().save()
        print(f'**kwargs: {kwargs}')
        # print(f'self.get_fields: {self.get_fields()}')
        print(f'type_self.instance: {type(self.instance.avatar.file.file)}')
        base_image = Image.open(self.instance.avatar.file.file)
        watermarked_image = put_watermark(base_image)
        watermarked_image = Image.open(watermarked_image)
        print(f'watermarked_image_after_Image.open(): {type(watermarked_image)}')
        watermarked_image.show()
        # watermarked_image = File(watermarked_image)
        print(f'watermarked_image: {watermarked_image}')
        self.instance.avatar.file.file = File(watermarked_image)
        return self.instance
