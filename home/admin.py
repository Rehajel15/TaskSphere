from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Group, Table, Table_taskColumn, Table_task

class TableTaskInline(admin.TabularInline):
    model = Table_task
    extra = 1

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "current_column":
            # request._obj_ wird im TableAdmin gesetzt
            if hasattr(request, '_obj_') and request._obj_ is not None:
                field.queryset = Table_taskColumn.objects.filter(table=request._obj_)
            else:
                field.queryset = Table_taskColumn.objects.none()
        return field

class TableTaskColumnInline(admin.TabularInline):
    model = Table_taskColumn
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
    inlines = [TableTaskColumnInline, TableTaskInline]

    def get_form(self, request, obj=None, **kwargs):
        # Übergibt das aktuelle Objekt an das Inline, damit das Queryset gefiltert werden kann
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Group, GroupAdmin)
admin.site.register(Table, TableAdmin)

