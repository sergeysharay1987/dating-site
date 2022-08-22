from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
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

app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак


class DetailClientApiView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]


class ListClientsApiView(ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]
