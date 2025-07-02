from django.urls import path
from .views import (
    HomeView, resumoView, nkgCreateView, velosogreenCreateView, volcafeCreateView,
    equipamento_listvolcafe_view, equipamento_listvelosogreen_view, velosocCreateView,
    CustomLoginView, carmocofeCreateView, expocacerCreateView, coxupeCreateView,
    CustomLogoutView, equipamento_listcoxupe_view, equipamento_listtexpo_view,
    equipamento_listcarmo_view, MapaView, get_t42_data, get_assetscontrols_data,
    AltocafezalCreateView, equipamento_list_view, burbomcofeCreateView,
    equipamento_listburbom_view, equipamento_listnkg_view, equipamento_listvelosocofe_view,
    update_assetscontrols_data, update_t42_data, verificar_fdoor
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("mapa/", MapaView.as_view(), name="mapa"),
    path("resumo/", resumoView, name="resumo"),
    
    # APIs
    path('api/get_t42_data/', get_t42_data, name="get_t42_data"),
    path('api/get_assetscontrols_data/', get_assetscontrols_data, name="get_assetscontrols_data"),
    path('api/assetscontrols/<str:asset_id>/', update_assetscontrols_data, name='update_assetscontrols_data'),
    path('api/t42/<str:unit_id>/', update_t42_data, name='update_t42_data'),
    path('api/equipamentos/', equipamento_list_view, name='get_equipamentos'),
    
    # Cadastros
    path('cadastrar/', AltocafezalCreateView.as_view(), name='altocafezal_cadastrar'),
    path('cadastrar/burbom', burbomcofeCreateView.as_view(), name='burbomcofe_cadastrar'),
    path('cadastrar/carmo', carmocofeCreateView.as_view(), name='carmocofe_cadastrar'),
    path('cadastrar/expo', expocacerCreateView.as_view(), name='expocacer_cadastrar'),
    path('cadastrar/coxu', coxupeCreateView.as_view(), name='coxupe_cadastrar'),
    path('cadastrar/nkg', nkgCreateView.as_view(), name='nkg_cadastrar'),     
    path('cadastrar/velosoc', velosocCreateView.as_view(), name='velosoc_cadastrar'),     
    path('cadastrar/velosog', velosogreenCreateView.as_view(), name='velosog_cadastrar'),     
    path('cadastrar/volcafe', volcafeCreateView.as_view(), name='volcafe_cadastrar'),     
    
    # Mapas
    path('equipamentos/', equipamento_list_view, name='altocafezal_mapa'),
    path('equipamentos/burbom', equipamento_listburbom_view, name='burbom_mapa'),
    path('equipamentos/carmo', equipamento_listcarmo_view, name='carmo_mapa'),
    path('equipamentos/expo', equipamento_listtexpo_view, name='expo_mapa'),
    path('equipamentos/coxu', equipamento_listcoxupe_view, name='coxu_mapa'),
    path('equipamentos/nkg', equipamento_listnkg_view, name='nkg_mapa'),
    path('equipamentos/velosoc', equipamento_listvelosocofe_view, name='velosoc_mapa'),
    path('equipamentos/velosog', equipamento_listvelosogreen_view, name='velosog_mapa'),   
    path('equipamentos/volcafe', equipamento_listvolcafe_view, name='volcafe_mapa'),
    
    #api
     path('verificar-fdoor/', verificar_fdoor, name='verificar_fdoor'),
]
