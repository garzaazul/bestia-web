"""
Leads - Configuración del Admin
"""
from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin configuration for Lead model."""
    
    list_display = ['name', 'company', 'email', 'interest', 'status', 'created_at']
    list_filter = ['status', 'interest', 'source', 'created_at']
    search_fields = ['name', 'email', 'company', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información de contacto', {
            'fields': ('name', 'email', 'company', 'position', 'phone')
        }),
        ('Interés', {
            'fields': ('interest', 'message', 'source')
        }),
        ('Seguimiento', {
            'fields': ('status', 'notes')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
