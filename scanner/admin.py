from django.contrib import admin
from .models import Equipamento

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'tipo_equipamento', 'data_recebido', 'peso_liquido', 'peso_bruto']
    list_filter = ['tipo_equipamento', 'data_recebido']
    search_fields = ['codigo']
    readonly_fields = ['tipo_equipamento', 'data_recebido']
    ordering = ['-data_recebido']