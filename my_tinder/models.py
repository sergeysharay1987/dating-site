from enum import Enum

from django.contrib.auth.base_user import BaseUserManager
from django.db.models import CharField, ImageField, EmailField, ForeignKey, CASCADE
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Пользовательский менеджер моделей, где электронная почта является уникальным идентификатором
    для аутентификации вместо имен пользователей.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет пользователя с заданным адресом электронной почты и паролем.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет суперпользователя с заданным адресом электронной почты и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Gender(Enum):

    FEMALE = 'M'
    MALE = 'F'


class CustomUser(AbstractUser):
    username = None
    email = EmailField(verbose_name='Email', unique=True)

    MALE = 'Male'
    FEMALE = 'Female'

    GENDERS = ((MALE, 'Female'),
               (FEMALE, 'Male'))

    avatar = ImageField(verbose_name='Photo', upload_to='photos/%Y/%m/%d')
    gender = CharField(verbose_name='Gender', max_length=1, choices=[(gender, gender.value) for gender in Gender])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    liked_users = ForeignKey('self', on_delete=CASCADE, blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
