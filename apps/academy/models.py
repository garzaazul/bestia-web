"""
Academy - Modelos para el programa de IAlfabetización
"""
from django.db import models


class WaitlistEntry(models.Model):
    """
    Lista de espera para el programa de formación 2026.
    Captura interesados desde el botón "Unirme a la Lista de Espera".
    """
    
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Nombre', max_length=100, blank=True)
    company = models.CharField('Empresa', max_length=100, blank=True)
    position = models.CharField('Cargo', max_length=100, blank=True)
    
    # Información adicional
    employees_count = models.CharField(
        'Tamaño de empresa',
        max_length=20,
        choices=[
            ('1-10', '1-10 empleados'),
            ('11-50', '11-50 empleados'),
            ('51-200', '51-200 empleados'),
            ('200+', 'Más de 200 empleados'),
        ],
        blank=True
    )
    
    # Estado
    is_confirmed = models.BooleanField('Email confirmado', default=False)
    is_enrolled = models.BooleanField('Inscrito en programa', default=False)
    
    # Metadatos
    created_at = models.DateTimeField('Fecha de registro', auto_now_add=True)
    notes = models.TextField('Notas', blank=True)
    
    class Meta:
        verbose_name = 'Inscripción lista de espera'
        verbose_name_plural = 'Lista de espera'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.company or 'Sin empresa'}"


class CourseModule(models.Model):
    """
    Módulos del programa de IAlfabetización.
    Placeholder para futura gestión de contenido.
    """
    
    title = models.CharField('Título', max_length=200)
    order = models.PositiveIntegerField('Orden', default=0)
    description = models.TextField('Descripción')
    is_active = models.BooleanField('Activo', default=True)
    
    class Meta:
        verbose_name = 'Módulo del curso'
        verbose_name_plural = 'Módulos del curso'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.order}. {self.title}"
