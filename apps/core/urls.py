"""
Core URLs - Rutas principales del sitio
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('nosotros/', views.about, name='about'),
    path('privacidad/', views.privacy_policy, name='privacy'),
]
