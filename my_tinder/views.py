from django.contrib.gis.measure import D
from django.core.mail import send_mail
from django.http import Http404
from rest_framework import viewsets
from dating_site.settings import EMAIL_HOST_USER
from .serializers import CreateUserSerializer, UserDetailSerializer
from rest_framework.authentication import TokenAuthentication
from my_tinder.models import CustomUser
from rest_framework.parsers import FileUploadParser, MultiPartParser
from my_tinder.permissions import IsUserPkInUrl
from django_filters import rest_framework as filters
from dj_rest_auth.views import *
from rest_framework.decorators import action


class CustomUserFilter(filters.FilterSet):
    first_name = filters.CharFilter(lookup_expr='startswith')
    last_name = filters.CharFilter(lookup_expr='startswith')
    location = filters.NumberFilter(lookup_expr='distance_lte', method='filter_location')

    class Meta:
        model = get_user_model()
        fields = ('gender', 'first_name', 'last_name')

    def filter_location(self, queryset, name, value):
        # construct the full lookup expression.
        user_point = self.request.user.location
        name = 'location'
        lookup = '__'.join([name, 'distance_lte'])
        return queryset.filter(**{lookup: (user_point, D(km=value))})


class ClientViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    authentication_classes = [
        TokenAuthentication,
    ]
    parses_classes = [
        MultiPartParser,
        FileUploadParser,
    ]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CustomUserFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'delete']:
            return UserDetailSerializer
        else:
            return CreateUserSerializer

    # def get_queryset(self):
    #     # print(f'self.request.query_params["distance"]: {self.request.query_params}')
    #     if self.action == 'list':
    #         # if self.request.query_params['distance']:
    #         #     distance = self.request.query_params['distance']
    #         #     auth_user = self.request.user
    #         #     auth_user_location = auth_user.location
    #         #     return CustomUser.objects.filter(location__distance_lte=(auth_user_location,
    #         D(km=distance))).exclude(
    #         #         id=auth_user.id)
    #
    #         return super().get_queryset().exclude(id=self.request.user.id)
    #     else:
    #         return super().get_queryset()

    def get_permissions(self):

        if self.action in ['retrieve', 'list', 'add_liked_user']:
            self.permission_classes = [IsAuthenticated]

        if self.action == 'create':
            self.permission_classes = [
                AllowAny,
            ]
        elif self.action in ['update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsUserPkInUrl]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_liked_user(self, request, pk=None):

        auth_user: CustomUser = request.user
        try:
            user = get_user_model().objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        if auth_user == user:
            return Response({'Предупреждение': 'Вы не можете поставить симпатию сами себе'})
        if auth_user.liked_users.contains(user) and auth_user != user:

            return Response({'Симпатия': f'Вам нравится пользователь {user.email}'})
        else:

            send_mail(
                subject='Симпатия',
                message=f'Вы понравились {auth_user.email}! Почта участника: {user.email}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[
                    user.email,
                ]
            )
            auth_user.liked_users.add(user)
            return Response({'Успех': f'Вы поставили симпатию пользователю {user.email}'})
