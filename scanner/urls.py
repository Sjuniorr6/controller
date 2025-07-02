from django.urls import path
from . import views

urlpatterns = [
    path('', views.scanner_view, name='scanner'),
    path('salvar/', views.salvar_codigo, name='salvar_codigo'),
]
