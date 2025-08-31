from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'biography', 'profile_picture', 'group',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'biography', 'profile_picture', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'is_staff', 'is_superuser',)
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)
