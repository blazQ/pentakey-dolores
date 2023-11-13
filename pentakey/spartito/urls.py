from django.urls import path
from . import views

urlpatterns = [
    path('accesso_upload/', views.accesso_pagina_upload, name='accesso_upload'),
    path('upload/', views.upload_spartito, name='upload_spartito'),
    path('download/<int:pk>/', views.download_spartito, name='download_spartito'),
    path('downloadmxml/', views.download_file, name='download_file'),
]