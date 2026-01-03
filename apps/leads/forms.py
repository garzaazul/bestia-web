"""
Leads - Formularios
"""
from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    """
    Formulario para captura de leads desde la web.
    Usado en el botón "Agendar Diagnóstico".
    """
    
    class Meta:
        model = Lead
        fields = ['name', 'email', 'company', 'position', 'phone', 'interest', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Tu nombre completo',
                'class': 'form-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'email@empresa.com',
                'class': 'form-input',
            }),
            'company': forms.TextInput(attrs={
                'placeholder': 'Nombre de tu empresa',
                'class': 'form-input',
            }),
            'position': forms.TextInput(attrs={
                'placeholder': 'Tu cargo (opcional)',
                'class': 'form-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+56 9 XXXX XXXX',
                'class': 'form-input',
            }),
            'interest': forms.Select(attrs={
                'class': 'form-select',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos brevemente tu situación actual...',
                'class': 'form-textarea',
                'rows': 4,
            }),
        }
