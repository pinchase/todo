from django.contrib import admin
from .models import Task, EmailVerification
from django.utils.html import format_html


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'user',
        'priority_badge',
        'category_badge',
        'due_date_display',
        'completed',
        'created_at'
    )
    list_filter = ('completed', 'priority', 'category', 'created_at', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('completed',)
    readonly_fields = ('created_at', 'updated_at', 'is_overdue')
    ordering = ('-created_at',)
    date_hierarchy = 'due_date'

    fieldsets = (
        ('Task Information', {
            'fields': ('user', 'title', 'description')
        }),
        ('Classification', {
            'fields': ('priority', 'category', 'due_date')
        }),
        ('Status', {
            'fields': ('completed', 'is_overdue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def priority_badge(self, obj):
        colors = {
            'low': '#10b981',
            'medium': '#f59e0b',
            'high': '#ef4444',
            'urgent': '#dc2626'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 5px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.priority, '#6b7280'),
            obj.get_priority_display()
        )

    priority_badge.short_description = 'Priority'

    def category_badge(self, obj):
        return format_html(
            '<span style="background: #4f46e5; color: white; padding: 3px 10px; border-radius: 5px; font-size: 11px;">{}</span>',
            obj.get_category_display()
        )

    category_badge.short_description = 'Category'

    def due_date_display(self, obj):
        if not obj.due_date:
            return '-'
        if obj.is_overdue:
            return format_html(
                '<span style="color: #dc2626; font-weight: bold;">⚠️ {}</span>',
                obj.due_date.strftime('%b %d, %Y')
            )
        return obj.due_date.strftime('%b %d, %Y')

    due_date_display.short_description = 'Due Date'


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