from django.db.models import CASCADE, CharField, ImageField, ManyToManyField, OneToOneField, TextChoices
from django.db import models
from dating_site.settings import AUTH_USER_MODEL


class Gender(TextChoices):
    MALE = 'М', 'Мужчина'
    FEMALE = 'Ж', 'Женщина'


class CustomUser(models.Model):
    user = OneToOneField(AUTH_USER_MODEL, on_delete=CASCADE)
    avatar = ImageField(verbose_name='Фото', upload_to='photos/%Y/%m/%d', blank=True, null=True)
    gender = CharField(verbose_name='Пол', max_length=1, choices=Gender.choices)
    liked_users = ManyToManyField(AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='liked_users_set')
    unliked_users = ManyToManyField(AUTH_USER_MODEL, blank=True, symmetrical=False, related_name='unliked_users_set')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
