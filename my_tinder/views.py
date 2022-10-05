from smtplib import SMTP

from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from dating_site.settings import EMAIL_HOST_USER
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from my_tinder.models import CustomUser
from rest_framework.parsers import MultiPartParser, FileUploadParser
from my_tinder.permissions import IsUserPkInUrl


class ClientViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication, ]
    parses_classes = [MultiPartParser, FileUploadParser, ]

    def get_permissions(self):

        if self.action in ['retrieve', 'list', 'add_liked_user']:
            self.permission_classes = [IsAuthenticated]

        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsUserPkInUrl]
        return super().get_permissions()

    def add_liked_user(self, request, pk=None):

        auth_user: CustomUser = request.user
        user = CustomUser.objects.get(pk=pk)
        if auth_user.liked_users.contains(user) and auth_user != user:

            return Response({'Симпатия': f'Вам нравится пользователь {user.email}'})
        else:

            send_mail(subject='Симпатия',
                      message='Вы понраивлись {auth_user.email}! Почта участника: {user.email}',
                      from_email=EMAIL_HOST_USER,
                      recipient_list=[user.email, ], auth_user=EMAIL_HOST_USER)
            auth_user.liked_users.add(user)
            return Response({'Успех': f'Вы поставили симпатию пользователю {user.email}'})
