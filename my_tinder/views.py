from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, GenericAPIView, UpdateAPIView, DestroyAPIView
from django.shortcuts import render, get_object_or_404, redirect
from .serializers import CustomUserSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class APIViewMixin(GenericAPIView):

    def dispatch(self, request, *args, **kwargs):

        token = Token.objects.get(user=request.user).key
        request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
        return super().dispatch(request, *args, **kwargs)


class ListClientsAPIView(APIViewMixin, ListAPIView):
    serializer_class = CustomUserSerializer

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]

    def get_queryset(self):

        queryset = CustomUser.objects.all()
        return queryset.exclude(id=self.request.user.id)


class DetailClientAPIView(APIViewMixin, RetrieveAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]


class UpdateClientAPIView(APIViewMixin, UpdateAPIView):
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]


class DestroyClientAPIView(DestroyAPIView):

    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminUser,)
    authentication_classes = [TokenAuthentication, ]
