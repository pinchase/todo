from django.contrib import admin
from .models import Task, EmailVerification


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('completed',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Status', {
            'fields': ('completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'created_at', 'verified_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at', 'verified_at')

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Verification Status', {
            'fields': ('is_verified', 'verified_at')
        }),
        ('Token', {
            'fields': ('token', 'created_at'),
            'classes': ('collapse',)
        }),
    )