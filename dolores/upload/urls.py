from django.urls import path
from . import views

urlpatterns = [
    path('', views.carica_partitura, name='carica_partitura'),
]
