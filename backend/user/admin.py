from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'is_phone', 'is_email', 'is_superuser')
    filter_horizontal = ()
    list_filter = ('is_phone', 'is_email', 'is_superuser')
    fieldsets = ()
    search_fields = ('username',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username',)


admin.site.register(User, UserAdmin)


admin.site.register(Profile, ProfileAdmin)
