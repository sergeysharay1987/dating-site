from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated], url_name='match')
    def check_match(self, request, pk=None):
        client = CustomUser.objects.get(pk=pk)
        return Response({'client': client})

    def get_permissions(self):

        if self.action in ['retrieve', 'list']:
            self.permission_classes = [IsAuthenticated]

        if self.action == 'create':
            self.permission_classes = [AllowAny, ]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsUserPkInUrl]
        return super().get_permissions()
