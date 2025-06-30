# urls.py
from django.urls import path
from .views import (
    EquipamentoListView,
    equipamentos_json,
    EquipamentoCreateView,
    EquipamentoUpdateView,
    EquipamentoDeleteView,
    dashboard,
    lista_equipamentos_api,
    EquipamentoListAPIView,
    atualizar_equipamento,
    atualizar_campos_modal,
    sincronizar_dados_t42,
    campos_banco_api,
)

urlpatterns = [
    # Lista de Equipamentos (Página principal)
    path("equipamentos/", EquipamentoListView.as_view(), name="equipamento_list"),

    # Criar
    path("novo/", EquipamentoCreateView.as_view(), name="equipamento_create"),

    # Editar
    path("<int:pk>/editar/", EquipamentoUpdateView.as_view(), name="equipamento_update"),

    # Deletar
    path("<int:pk>/deletar/", EquipamentoDeleteView.as_view(), name="equipamento_delete"),

    # Dashboard
    path("dashboard/", dashboard.as_view(), name="dashboard_view"),

    # API de lista de equipamentos (Função)
    path("api/equipamentos/", lista_equipamentos_api, name="api_equipamentos"),

    # API de lista de equipamentos (APIView) -- se quiser rota separada
    path("api/equipamentos/list/", EquipamentoListAPIView.as_view(), name="api_equipamentos_list"),

    # Atualizar Equipamento (Função)
    path("equipamentos/update/", atualizar_equipamento, name="atualizar_equipamento"),

    # Atualizar campos do modal (BL, Container, Destino)
    path("api/atualizar-campos-modal/", atualizar_campos_modal, name="atualizar_campos_modal"),

    # Sincronizar dados da API T42
    path("api/sincronizar-t42/", sincronizar_dados_t42, name="sincronizar_dados_t42"),

    # Retorna JSON de equipamentos (outra rota)
    path("equipamentos-json/", equipamentos_json, name="equipamentos_json"),

    # API para retornar campos do banco
    path("api/campos-banco/", campos_banco_api, name="campos_banco_api"),

    # Atualizar status via JS (POST)
  

]
