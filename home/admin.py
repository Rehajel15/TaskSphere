from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Group, Table, Table_task
from .forms import CreateTaskForm
from authentication.forms import CreateGroupForm

class TableTaskInline(admin.TabularInline):
    model = Table_task
    form = CreateTaskForm
    extra = 1


    
class TableInline(admin.TabularInline):
    model = Table
    extra = 1  

    def has_add_permission(self, request, obj=None):
        return False

    
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'givenID', 'group_biography', 'group_password', 'created_on', 'id',)
    readonly_fields = ('created_on', 'get_users', 'id')
    search_fields = ('group_name', 'givenID')
    form = CreateGroupForm
    inlines = [TableInline]


    def get_users(self, obj):
        if obj.users.exists():
            return format_html("<br>".join([user.email for user in obj.users.all()]))
        return "No users"

    get_users.short_description = 'Users'


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'group')
    search_fields = ('id', 'group__givenID')
    readonly_fields = ('id', 'group')
    inlines = [TableTaskInline]

    def get_form(self, request, obj=None, **kwargs):
        # Übergibt das aktuelle Objekt an das Inline, damit das Queryset gefiltert werden kann
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Group, GroupAdmin)
admin.site.register(Table, TableAdmin)

