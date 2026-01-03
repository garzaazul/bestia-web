"""
Leads - Vistas para formularios de contacto
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import LeadForm


def contact(request):
    """
    Vista para el formulario de contacto/diagnóstico.
    """
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save()
            
            # Si es AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': '¡Gracias! Nos pondremos en contacto pronto.'
                })
            
            # Redirección normal con mensaje
            messages.success(
                request,
                '¡Gracias por tu interés! Nos pondremos en contacto contigo pronto.'
            )
            return redirect('core:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = LeadForm()
    
    return render(request, 'leads/contact.html', {'form': form})
