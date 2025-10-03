from django.contrib import admin
from .models import Task


# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('completed',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Task Information',{
        'fields': ('user', 'title', 'description')
        }),
        ('Status',{
        'fields': ('completed',)
        }),
        ('Timestamps',{
        'fields': ('created_at', 'updated_at'),
        'classes': ('collapse',)
        }),
    )