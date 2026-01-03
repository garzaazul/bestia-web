"""
Core views - Home y páginas estáticas
"""
from django.shortcuts import render


def home(request):
    """
    Vista principal de la home page.
    Renderiza el template con toda la información de bestIA.
    """
    context = {
        'page_title': 'bestIA Engineering - Soluciones de IA B2B',
        'meta_description': 'Ingeniería de Inteligencia Artificial para empresas. '
                           'Agentes autónomos, automatización, consultoría y formación profesional.',
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """Vista de 'Nosotros' (si se separa de la home)"""
    return render(request, 'pages/about.html')


def privacy_policy(request):
    """Política de privacidad"""
    return render(request, 'pages/privacy.html')
