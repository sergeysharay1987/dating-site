from django import template
from ..models import CustomUser

register = template.Library()


@register.simple_tag
def get_verbose_field_name(instance: CustomUser, field_name: str):
    """
    Возвращает verbose_name для каждого поля модели.
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.simple_tag
def get_liked_users(instance: CustomUser, obj):
    """
    Возвращает QuerySet дочерней модели.
    """
    return instance.customuser_set.contains(obj)
