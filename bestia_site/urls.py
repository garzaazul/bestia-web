"""
URL configuration for bestia_site project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps
    path('', include('apps.core.urls')),           # Home y páginas estáticas
    path('leads/', include('apps.leads.urls')),    # Formularios de contacto
    path('academy/', include('apps.academy.urls')), # IAlfabetización
    path('chat/', include('apps.chat.urls')),      # Futuro chatbot
]
