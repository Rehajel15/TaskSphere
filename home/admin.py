# admin.py
from django.contrib import admin
from .models import Group, Table, Table_taskColumn, Table_task

class Table_taskColumnInline(admin.TabularInline):
    model = Table_taskColumn
    extra = 1

class Table_taskInline(admin.TabularInline):
    model = Table_task
    extra = 1

class TableInline(admin.TabularInline):
    model = Table
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [TableInline]

class TableAdmin(admin.ModelAdmin):
    inlines = [Table_taskColumnInline, Table_taskInline]

admin.site.register(Group, GroupAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Table_taskColumn)
admin.site.register(Table_task)

