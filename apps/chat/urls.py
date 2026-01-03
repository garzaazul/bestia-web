"""
Chat - URLs
"""
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_interface, name='interface'),
    path('message/', views.send_message, name='send_message'),
    path('history/', views.get_history, name='history'),
]
