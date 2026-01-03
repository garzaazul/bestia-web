"""
Academy - URLs
"""
from django.urls import path
from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.program, name='program'),
    path('waitlist/', views.join_waitlist, name='waitlist'),
]
