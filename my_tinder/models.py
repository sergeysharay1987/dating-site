from cuser.models import AbstractCUser
from django.db.models import CharField, ImageField, ManyToManyField, TextChoices
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db import models


class Gender(TextChoices):
    MALE = 'M', 'Men'
    FEMALE = 'F', 'Female'


class CustomUser(AbstractCUser):
    avatar = ImageField(verbose_name='Photo', upload_to='photos/%Y/%m/%d', blank=True, null=True)
    gender = CharField(verbose_name='Gender', max_length=1, choices=Gender.choices)
    first_name = CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = CharField(_('last name'), max_length=150, blank=True, null=True)
    liked_users = ManyToManyField('self', blank=True, symmetrical=False, related_name='liked_users_set')
    unliked_users = ManyToManyField('self', blank=True, symmetrical=False, related_name='unliked_users_set')
    location = models.PointField(blank=True, null=True, srid=4326, geography=True)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
