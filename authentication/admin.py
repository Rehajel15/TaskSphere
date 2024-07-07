from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('biography', 'profile_picture', 'in_group')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'biography', 'profile_picture', 'in_group', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'is_superuser', 'in_group')
    search_fields = ('email', 'biography')
    ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)
