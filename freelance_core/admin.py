from django.contrib import admin
from .models import Client, Project, Task

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'user')
    search_fields = ('name', 'company', 'email')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'status', 'start_date')
    list_filter = ('status', 'client')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'project')
