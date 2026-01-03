"""
Academy - Configuración del Admin
"""
from django.contrib import admin
from .models import WaitlistEntry, CourseModule


@admin.register(WaitlistEntry)
class WaitlistEntryAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'company', 'is_confirmed', 'is_enrolled', 'created_at']
    list_filter = ['is_confirmed', 'is_enrolled', 'employees_count', 'created_at']
    search_fields = ['email', 'name', 'company']
    readonly_fields = ['created_at']


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ['order', 'title', 'is_active']
    list_display_links = ['title']
    list_editable = ['order', 'is_active']
    ordering = ['order']
