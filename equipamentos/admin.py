from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Equipamento

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'modelo', 'cliente', 'data_entrega', 'status_operacao')
    search_fields = ('identificador', 'cliente', 'modelo')
    list_filter = ('status_operacao', 'data_entrega')
