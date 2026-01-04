"""
Chat - Modelos para el chatbot con IA

Arquitectura preparada para:
- Integración con LLMs (OpenAI, Anthropic, etc.)
- RAG con base de conocimiento propia
- Historial de conversaciones persistente
- Análisis de interacciones
"""
import uuid
from django.db import models


class ChatSession(models.Model):
    """
    Sesión de chat con un usuario.
    Agrupa mensajes de una conversación.
    """
    
    # Identificador único para URLs públicas (no expone IDs internos)
    session_id = models.UUIDField(
        'ID de sesión',
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    
    # Opcional: vincular a usuario autenticado o email
    user_email = models.EmailField('Email del usuario', blank=True, null=True)
    user_name = models.CharField('Nombre', max_length=100, blank=True)
    
    # Persistencia de Chat (Gemini History)
    history = models.JSONField(
        'Historial',
        default=list,
        blank=True,
        help_text='Historial completo de la conversación (formato Gemini)'
    )
    summary = models.TextField('Resumen', blank=True, null=True)
    
    # Metadatos de la sesión
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Última actividad', auto_now=True)
    
    # Contexto adicional (JSON flexible para futura expansión)
    metadata = models.JSONField(
        'Metadatos',
        default=dict,
        blank=True,
        help_text='Contexto adicional: IP, user-agent, fuente, etc.'
    )
    
    # Estado de la sesión
    is_active = models.BooleanField('Activa', default=True)
    
    # Para análisis
    total_messages = models.PositiveIntegerField('Total mensajes', default=0)
    
    class Meta:
        verbose_name = 'Sesión de chat'
        verbose_name_plural = 'Sesiones de chat'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Sesión {self.session_id} - {self.user_email or 'Anónimo'}"


class ChatMessage(models.Model):
    """
    Mensaje individual dentro de una conversación.
    Almacena tanto mensajes del usuario como respuestas del asistente.
    """
    
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),  # Para prompts de contexto
    ]
    
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Sesión'
    )
    
    role = models.CharField('Rol', max_length=20, choices=ROLE_CHOICES)
    content = models.TextField('Contenido')
    
    # Timestamps
    created_at = models.DateTimeField('Enviado', auto_now_add=True)
    
    # Para RAG: referencia a embeddings/documentos recuperados
    embedding_id = models.CharField(
        'ID de embedding',
        max_length=100,
        blank=True,
        null=True,
        help_text='Referencia a vector DB (Pinecone, Qdrant, pgvector)'
    )
    
    # Documentos/fuentes usadas para generar respuesta (RAG)
    sources = models.JSONField(
        'Fuentes',
        default=list,
        blank=True,
        help_text='Lista de documentos/chunks usados para la respuesta'
    )
    
    # Metadatos del mensaje (tokens usados, modelo, etc.)
    metadata = models.JSONField(
        'Metadatos',
        default=dict,
        blank=True,
        help_text='Tokens, modelo usado, latencia, etc.'
    )
    
    class Meta:
        verbose_name = 'Mensaje de chat'
        verbose_name_plural = 'Mensajes de chat'
        ordering = ['created_at']
    
    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f"[{self.role}] {preview}"


class KnowledgeDocument(models.Model):
    """
    Placeholder para documentos de la base de conocimiento (RAG).
    Permite indexar documentos propios para el chatbot.
    """
    
    title = models.CharField('Título', max_length=200)
    content = models.TextField('Contenido')
    source_url = models.URLField('URL de origen', blank=True)
    
    # Categorización
    category = models.CharField(
        'Categoría',
        max_length=50,
        choices=[
            ('services', 'Servicios'),
            ('academy', 'IAlfabetización'),
            ('faq', 'Preguntas frecuentes'),
            ('company', 'Empresa'),
            ('technical', 'Documentación técnica'),
        ],
        default='faq'
    )
    
    # Estado de indexación
    is_indexed = models.BooleanField('Indexado en vector DB', default=False)
    indexed_at = models.DateTimeField('Fecha de indexación', blank=True, null=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('Activo', default=True)
    
    class Meta:
        verbose_name = 'Documento de conocimiento'
        verbose_name_plural = 'Base de conocimiento'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
