from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import CustomUserSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from dating_site.settings import BASE_DIR
from .apps import MyTinderConfig
from PIL import Image
from my_tinder.models import CustomUser
from .forms import CreateClientForm
from .my_tinder_services.put_watermark import put_watermark
from rest_framework.authtoken.models import Token


app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак


class DetailClientApiView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def dispatch(self, request, *args, **kwargs):

        if isinstance(request.user, CustomUser):
            token = Token.objects.get(user=request.user).key
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'

        return super().dispatch(request, *args, **kwargs)


class ListClientsApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def dispatch(self, request, *args, **kwargs):

        if isinstance(request.user, CustomUser):
            token = Token.objects.get(user=request.user).key
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
        return super().dispatch(request, *args, **kwargs)

