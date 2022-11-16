from django.contrib import admin
from django.contrib.auth import get_user_model
from cuser.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'gender', 'first_name', 'last_name')
    list_display_links = (
        'email',
        'first_name',
    )
    search_fields = ('email', 'gender')


admin.site.register(get_user_model(), CustomUserAdmin)
