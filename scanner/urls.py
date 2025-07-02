

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar/', views.registrar_equipamento, name='registrar_equipamento'),
]