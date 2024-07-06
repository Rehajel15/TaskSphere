from django.contrib import admin
from authentication.models import ExtendedUserInformation

# Register your models here.

class ExtendedUserInformationAdmin(admin.ModelAdmin):
    list_display = ('biography', 'profile_picture', 'in_group',)
    search_fields = ('user__username',)
    readonly_fields = ('user',)

    def has_add_permission(self, request, obj=None):
        return False

admin.site.register(ExtendedUserInformation, ExtendedUserInformationAdmin)
