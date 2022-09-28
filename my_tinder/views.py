from io import BytesIO
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, UpdateAPIView, \
    DestroyAPIView
from rest_framework import viewsets, status
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from .serializers import CustomUserSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.authentication import TokenAuthentication
from dating_site.settings import BASE_DIR
from .apps import MyTinderConfig
from PIL import Image
from my_tinder.models import CustomUser
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.decorators import api_view, permission_classes
from .my_tinder_services.put_watermark import put_watermark
from my_tinder.permissions import IsUserPkInUrl

app_name = MyTinderConfig.name  # название приложения
watermark = 'watermark.png'  # название изображение, содержащее водяной знак
path_to_watermark = f'{BASE_DIR}/{app_name}/{watermark}'  # путь до изображения, содержащее водяной знак


class ClientViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # permission_classes = [IsAuthenticated, IsUserPkInUrl]
    authentication_classes = [TokenAuthentication, ]

    parses_classes = [MultiPartParser, FileUploadParser, ]

    def perform_create(self, serializer):

        base_image = serializer.validated_data["avatar"].file
        base_image = Image.open(base_image).convert('RGBA')
        watermark = Image.open(path_to_watermark)

        base_image.alpha_composite(watermark)
        bytes = BytesIO()
        base_image.save(bytes, 'PNG')
        serializer.validated_data["avatar"].file = bytes
        serializer.save()

