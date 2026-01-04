"""
Chat - Configuración del Admin
"""
from django.contrib import admin
from .models import ChatSession, ChatMessage, KnowledgeDocument


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['role', 'content', 'created_at', 'embedding_id']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user_email', 'total_messages', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['session_id', 'user_email', 'user_name']
    readonly_fields = ['session_id', 'created_at', 'updated_at', 'total_messages', 'history', 'summary']
    inlines = [ChatMessageInline]


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'content_preview', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['content', 'session__session_id']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Contenido'


@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_indexed', 'is_active', 'updated_at']
    list_filter = ['category', 'is_indexed', 'is_active']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'indexed_at']
