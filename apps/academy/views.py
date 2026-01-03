"""
Academy - Vistas para IAlfabetización
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from .models import WaitlistEntry


def program(request):
    """Vista del programa de IAlfabetización (si se separa de la home)."""
    return render(request, 'academy/program.html')


@require_POST
def join_waitlist(request):
    """
    Endpoint para unirse a la lista de espera.
    Soporta tanto AJAX como formulario tradicional.
    """
    email = request.POST.get('email', '').strip()
    name = request.POST.get('name', '').strip()
    company = request.POST.get('company', '').strip()
    
    if not email:
        return JsonResponse({
            'success': False,
            'error': 'El email es requerido.'
        }, status=400)
    
    try:
        WaitlistEntry.objects.create(
            email=email,
            name=name,
            company=company
        )
        return JsonResponse({
            'success': True,
            'message': '¡Te has unido a la lista de espera! Te contactaremos pronto.'
        })
    except IntegrityError:
        return JsonResponse({
            'success': False,
            'error': 'Este email ya está registrado en la lista de espera.'
        }, status=400)
