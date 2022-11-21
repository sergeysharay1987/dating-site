from django.contrib import admin
from django.contrib.auth import get_user_model
from cuser.admin import UserAdmin

# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('gender',)
    list_display_links = (
        'email',
        'first_name',
    )
    UserAdmin.fieldsets[1][1]['fields'] = UserAdmin.fieldsets[1][1]['fields'] + ('avatar', 'gender')
    fieldsets = UserAdmin.fieldsets


admin.site.register(get_user_model(), CustomUserAdmin)
