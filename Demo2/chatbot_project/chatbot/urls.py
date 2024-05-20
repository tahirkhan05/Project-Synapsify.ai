# chatbot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Example URL pattern
    path('get_response/', views.get_response, name='get_response'),
]
