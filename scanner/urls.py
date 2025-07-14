from django.urls import path
from . import views

app_name = 'scanner'

urlpatterns = [
    path('', views.index, name='scan'),
    path('registrar/', views.registrar_equipamento, name='registrar_equipamento'),
    path('historico/', views.historico_equipamentos, name='scan_historico'),
]
