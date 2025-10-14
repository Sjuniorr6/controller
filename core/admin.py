from django.contrib import admin
from .models import EventoTratado, PosicaoEquipamento, AlertaGeofencing


@admin.register(EventoTratado)
class EventoTratadoAdmin(admin.ModelAdmin):
    list_display = ['guid', 'tipo_evento', 'valor', 'status', 'alerta_disparado', 'criado_em']
    list_filter = ['tipo_evento', 'status', 'alerta_disparado', 'criado_em']
    search_fields = ['guid', 'nome_equipamento']
    readonly_fields = ['criado_em']
    date_hierarchy = 'criado_em'


@admin.register(PosicaoEquipamento)
class PosicaoEquipamentoAdmin(admin.ModelAdmin):
    list_display = ['guid', 'nome_equipamento', 'latitude', 'longitude', 'dentro_de_cerca', 'nome_cerca', 'tipo_cerca', 'parado', 'timestamp']
    list_filter = ['dentro_de_cerca', 'tipo_cerca', 'parado', 'timestamp']
    search_fields = ['guid', 'nome_equipamento', 'nome_cerca']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Equipamento', {
            'fields': ('guid', 'nome_equipamento')
        }),
        ('Localização', {
            'fields': ('latitude', 'longitude', 'velocidade', 'parado')
        }),
        ('Geofencing', {
            'fields': ('dentro_de_cerca', 'nome_cerca', 'tipo_cerca')
        }),
        ('Timestamp', {
            'fields': ('timestamp',)
        }),
    )


@admin.register(AlertaGeofencing)
class AlertaGeofencingAdmin(admin.ModelAdmin):
    list_display = ['guid', 'nome_equipamento', 'tipo_alerta', 'nome_local', 'status', 'resolvido', 'dias_parado', 'criado_em']
    list_filter = ['tipo_alerta', 'status', 'resolvido', 'criado_em']
    search_fields = ['guid', 'nome_equipamento', 'nome_local']
    readonly_fields = ['criado_em', 'resolvido_em']
    date_hierarchy = 'criado_em'
    actions = ['marcar_como_tratado', 'resolver_alertas']
    
    fieldsets = (
        ('Equipamento', {
            'fields': ('guid', 'nome_equipamento', 'tipo_alerta')
        }),
        ('Local', {
            'fields': ('nome_local', 'latitude', 'longitude')
        }),
        ('Informações do Alerta', {
            'fields': ('saiu_em', 'parado_desde', 'dias_parado')
        }),
        ('Controle', {
            'fields': ('criado_em', 'alerta_disparado', 'resolvido', 'resolvido_em')
        }),
        ('Tratamento', {
            'fields': ('status', 'tratado_em', 'tratado_por', 'observacoes')
        }),
    )
    
    def marcar_como_tratado(self, request, queryset):
        """Marca alertas selecionados como tratados"""
        count = 0
        for alerta in queryset:
            alerta.marcar_como_tratado(
                tratado_por=request.user.username,
                observacoes="Marcado como tratado pelo admin"
            )
            count += 1
        self.message_user(request, f"{count} alerta(s) marcado(s) como tratado(s).")
    marcar_como_tratado.short_description = "Marcar como tratado"
    
    def resolver_alertas(self, request, queryset):
        """Resolve alertas selecionados"""
        count = 0
        for alerta in queryset:
            alerta.resolver()
            count += 1
        self.message_user(request, f"{count} alerta(s) resolvido(s).")
    resolver_alertas.short_description = "Resolver alertas"
