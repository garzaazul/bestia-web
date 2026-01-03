"""
Leads - Modelos para captura de contactos y leads
"""
from django.db import models


class Lead(models.Model):
    """
    Modelo para captura de leads de diagnóstico y consultoría.
    Almacena información de empresas interesadas en servicios de IA.
    """
    
    INTEREST_CHOICES = [
        ('solutions', 'Soluciones Empresas'),
        ('academy', 'IAlfabetización'),
        ('consulting', 'Consultoría Estratégica'),
        ('agents', 'Agentes Autónomos & RAG'),
        ('automation', 'Automatización (RPA + IA)'),
        ('other', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'Nuevo'),
        ('contacted', 'Contactado'),
        ('qualified', 'Calificado'),
        ('proposal', 'Propuesta enviada'),
        ('closed_won', 'Cerrado ganado'),
        ('closed_lost', 'Cerrado perdido'),
    ]
    
    # Información de contacto
    name = models.CharField('Nombre', max_length=100)
    email = models.EmailField('Email')
    company = models.CharField('Empresa', max_length=100, blank=True)
    position = models.CharField('Cargo', max_length=100, blank=True)
    phone = models.CharField('Teléfono', max_length=20, blank=True)
    
    # Interés y mensaje
    interest = models.CharField(
        'Área de interés',
        max_length=50,
        choices=INTEREST_CHOICES,
        default='solutions'
    )
    message = models.TextField('Mensaje', blank=True)
    
    # Estado y seguimiento
    status = models.CharField(
        'Estado',
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )
    notes = models.TextField('Notas internas', blank=True)
    
    # Metadatos
    created_at = models.DateTimeField('Fecha de creación', auto_now_add=True)
    updated_at = models.DateTimeField('Última actualización', auto_now=True)
    source = models.CharField(
        'Fuente',
        max_length=50,
        default='website',
        help_text='De dónde vino el lead (website, linkedin, referido, etc.)'
    )
    
    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.company or 'Sin empresa'} ({self.get_interest_display()})"
