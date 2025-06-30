from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Equipamento
from .forms import EquipamentoForm

# ✅ LISTAR EQUIPAMENTOS
from django.db.models.functions import Coalesce
from django.db.models import Value
from django.utils import timezone

from django.db.models.functions import Coalesce
from django.db.models import Value, DateTimeField
from datetime import datetime
from datetime import datetime, timezone
from django.db.models import Value, DateTimeField
from django.db.models.functions import Coalesce
from django.views.generic import ListView
from .models import Equipamento
from django.db.models import F

class EquipamentoListView(ListView):
    model = Equipamento
    template_name = "equipamento_list.html"
    context_object_name = "equipamentos"

    def get_queryset(self):
        # Sem Coalesce, sem loop, sem nada
        return Equipamento.objects.all()


# ✅ CRIAR EQUIPAMENTO
class EquipamentoCreateView(CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "equipamento_form.html"
    success_url = reverse_lazy("equipamento_list")  # Redirecionamento após criação

# ✅ EDITAR EQUIPAMENTO
class EquipamentoUpdateView(UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = "equipamento_form.html"
    success_url = reverse_lazy("equipamento_list")  # Redirecionamento após edição

# ✅ DELETAR EQUIPAMENTO
class EquipamentoDeleteView(DeleteView):
    model = Equipamento
    template_name = "equipamento_confirm_delete.html"
    success_url = reverse_lazy("equipamento_list")  # Redirecionamento após exclusão

# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Equipamento

class dashboard(ListView):
    model = Equipamento
    template_name = "relatorios.html"
    context_object_name = "equipamentos"  # Nome da variável no template
    ordering = ["-data_insercao"]  # Ordenação por data mais recente
    
    def get_queryset(self):
        equipamentos = Equipamento.objects.all()
        for equipamento in equipamentos:
            equipamento.atualizar_status_pela_localizacao()
        return equipamentos


from django.http import JsonResponse
from .models import Equipamento

from django.http import JsonResponse
from .models import Equipamento

def lista_equipamentos_api(request):
    # Obtém todos os equipamentos e converte para dicionários
    equipamentos = Equipamento.objects.all().values()
    # Retorna como JSON (list() para poder passar no JsonResponse)
    return JsonResponse(list(equipamentos), safe=False)





from django.http import JsonResponse
from .models import Equipamento
import math

# Se quiser usar a mesma lógica de distância do Leaflet, pode instequialar geopy ou você mesmo cria a fórmula
# ou faz um "mock" da distanceTo. Aqui, vamos usar a própria lógica do Leaflet se quiser,
# mas seria preciso instalar e importar ou escrever uma função de Haversine. 
# Para simplificar, usarei a fórmula de Haversine manualmente.

def distance_km(lat1, lon1, lat2, lon2):
    """
    Calcula distância (em metros) usando a fórmula de Haversine
    """
    R = 6371_000  # raio da Terra ~ 6371 km em metros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # retorna metros
    return R * c

CERCAS = [
    { "nome": "Carmocoffe", "coordenadas": [-21.6319, -45.2740], "raio": 8000, "cor": "red" },
    { "nome": "Alto Cafezal", "coordenadas": [-18.9484, -47.0058], "raio": 8000, "cor": "red" },
    { "nome": "BOURBON SPECIALTY COFFEES", "coordenadas": [-21.7804, -46.5690], "raio": 8000, "cor": "red" },
    { "nome": "COOXUPÉ", "coordenadas": [-21.2937, -46.7222], "raio": 500,  "cor": "red" },
    { "nome": "EXPOCACCER", "coordenadas": [-18.9455, -47.0071], "raio": 8000, "cor": "red" },
    { "nome": "NKG", "coordenadas": [-21.5771, -45.4721], "raio": 5800, "cor": "red" },
    { "nome": "VELOSO COFFEE", "coordenadas": [-18.9981, -46.3011], "raio": 8000, "cor": "red" },
    { "nome": "ANTUERPIA", "coordenadas": [51.2639, 4.41496], "raio": 8000, "cor": "green" },
    { "nome": "porto", "coordenadas": [51.3032, 4.2824], "raio": 8000, "cor": "green" },
    { "nome": "VOLCAFÉ", "coordenadas": [-21.5743, -45.4389], "raio": 8000, "cor": "red" },
    { "nome": "BREMEN", "coordenadas": [53.1208, 8.7345], "raio": 8000, "cor": "green" },
    { "nome": "AVENCHES", "coordenadas": [46.8938, 7.0514], "raio": 8000, "cor": "green" },
    { "nome": "BREMENPORT", "coordenadas": [53.0584, 8.8966], "raio": 8000, "cor": "green" },
    { "nome": "BREMENPORT2", "coordenadas": [53.1258, 8.7190], "raio": 8000, "cor": "green" },
    { "nome": "ROMONT", "coordenadas": [46.6806, 6.9051], "raio": 8000, "cor": "green" },
    { "nome": "BARCELONA", "coordenadas": [41.3504, 2.1635], "raio": 8000, "cor": "green" },
    { "nome": "orbe", "coordenadas": [46.7266, 6.5365], "raio": 8000, "cor": "green" }
]

def verificar_status(lat, lon):
    """
    Retorna 'Na Fazenda' se cor=red, 'No Destino' se cor=green, ou 'Em Viagem'
    """
    if lat is None or lon is None:
        return "Sem Coord."

    for cerca in CERCAS:
        lat_cerca, lon_cerca = cerca["coordenadas"]
        dist_metros = distance_km(lat, lon, lat_cerca, lon_cerca)  # retorna metros
        if dist_metros <= cerca["raio"]:
            return "Na Fazenda" if cerca["cor"] == "red" else "No Destino"
    return "Em Viagem"

def lista_equipamentos_api(request):
    """
    Retorna JSON de equipamentos com status calculado
    """
    equipamentos = Equipamento.objects.all()
    data = []
    for eq in equipamentos:
        # Calcule o status para cada eq
        lat = eq.latitude
        lon = eq.longitude
        status = verificar_status(lat, lon)

        data.append({
            "id": eq.id,
            "cliente": eq.cliente,
            "latitude": lat,
            "longitude": lon,
            "status": status,
            # inclua outros campos que desejar
        })

    return JsonResponse(data, safe=False)





from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Equipamento
from .serializers import EquipamentoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Equipamento
from .serializers import EquipamentoSerializer

class EquipamentoListAPIView(APIView):
    def get(self, request):
        equipamentos = Equipamento.objects.all()
        serializer = EquipamentoSerializer(equipamentos, many=True)
        return Response(serializer.data)

# views.py
from django.http import JsonResponse
from .models import Equipamento

def lista_equipamentos_api(request):
    equipamentos = Equipamento.objects.all().values()
    return JsonResponse(list(equipamentos), safe=False)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Equipamento

@csrf_exempt  # Permite requisições sem CSRF Token (não recomendado para produção sem proteção extra)
def atualizar_equipamento(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Pega os dados enviados via JSON
            
            equipamento = Equipamento.objects.get(identificador=data["identificador"])
            equipamento.status_operacao = data["status"]
            equipamento.save()

            return JsonResponse({"mensagem": "Equipamento atualizado com sucesso!"}, status=200)
        except Equipamento.DoesNotExist:
            return JsonResponse({"erro": "Equipamento não encontrado."}, status=404)
        except Exception as e:
            return JsonResponse({"erro": str(e)}, status=500)
    return JsonResponse({"erro": "Método não permitido"}, status=405)

@csrf_exempt
def atualizar_campos_modal(request):
    """
    Atualiza os campos BL, Container e Destino via AJAX
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("\n========== DEBUG atualizar_campos_modal ==========")
            print(f"JSON recebido: {data}")
            
            unitnumber = data.get("unitnumber")
            print(f"unitnumber recebido: {unitnumber}")
            if not unitnumber:
                print("[ERRO] unitnumber não enviado!")
                return JsonResponse({
                    "success": False,
                    "erro": "Unitnumber é obrigatório"
                }, status=400)
            
            equipamentos = Equipamento.objects.filter(identificador=unitnumber).order_by('-id')
            if equipamentos.exists():
                equipamento = equipamentos.first()  # O mais recente
                created = False
            else:
                equipamento = Equipamento(
                    identificador=unitnumber,
                    BL=data.get("BL", ""),
                    container=data.get("container", ""),
                    destino=data.get("destino", "")
                )
                created = True
            print(f"get_or_create: created={created} | equipamento.id={equipamento.id if hasattr(equipamento, 'id') else 'N/A'}")
            # Atualiza campos
            equipamento.BL = data.get("BL", "")
            equipamento.container = data.get("container", "")
            equipamento.destino = data.get("destino", "")
            lat = data.get("latitude", None)
            print(f"latitude recebido: {lat}")
            try:
                equipamento.latitude = float(lat) if lat not in (None, "") else equipamento.latitude
            except (ValueError, TypeError):
                print(f"[ERRO] latitude inválida: {lat}")
            lon = data.get("longitude", None)
            print(f"longitude recebido: {lon}")
            try:
                equipamento.longitude = float(lon) if lon not in (None, "") else equipamento.longitude
            except (ValueError, TypeError):
                print(f"[ERRO] longitude inválida: {lon}")
            print(f"Salvando: identificador={equipamento.identificador}, BL={equipamento.BL}, container={equipamento.container}, destino={equipamento.destino}, latitude={equipamento.latitude}, longitude={equipamento.longitude}")
            equipamento.save()
            print(f"[OK] Equipamento salvo/atualizado: {equipamento}")
            print("========== FIM DEBUG atualizar_campos_modal ==========")

            return JsonResponse({
                "success": True,
                "mensagem": "Campos atualizados com sucesso!",
                "dados": {
                    "unitnumber": equipamento.identificador,
                    "BL": equipamento.BL,
                    "container": equipamento.container,
                    "destino": equipamento.destino
                }
            }, status=200)
            
        except json.JSONDecodeError as e:
            print(f"[ERRO] JSONDecodeError: {str(e)}")
            return JsonResponse({
                "success": False,
                "erro": f"Erro ao decodificar JSON: {str(e)}"
            }, status=400)
        except Exception as e:
            print(f"[ERRO] Exception: {str(e)}")
            return JsonResponse({
                "success": False,
                "erro": f"Erro ao atualizar: {str(e)}"
            }, status=500)
    
    print("[ERRO] Método não permitido!")
    return JsonResponse({
        "success": False,
        "erro": "Método não permitido"
    }, status=405)



# views.py

from django.http import HttpResponse
from django.core import serializers
from .models import Equipamento

def equipamentos_json(request):
    """
    Retorna todos os registros de Equipamento em formato JSON.
    """
    equipamentos = Equipamento.objects.all()
    # Usamos o serializer embutido do Django para transformar em JSON
    data = serializers.serialize('json', equipamentos)
    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def sincronizar_dados_t42(request):
    """
    Sincroniza dados da API T42 com o banco de dados local
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print(f"Dados T42 recebidos para sincronização: {len(data)} equipamentos")
            
            equipamentos_atualizados = 0
            equipamentos_criados = 0
            
            for equipamento_data in data:
                unitnumber = equipamento_data.get('unitnumber')
                if not unitnumber:
                    continue
                equipamentos = Equipamento.objects.filter(identificador=unitnumber).order_by('-id')
                if equipamentos.exists():
                    equipamento = equipamentos.first()
                else:
                    equipamento = Equipamento(identificador=unitnumber)
                    equipamentos_criados += 1
                equipamento.latitude = equipamento_data.get('latitude')
                equipamento.longitude = equipamento_data.get('longitude')
                equipamento.BL = equipamento_data.get('BL', equipamento.BL)
                equipamento.container = equipamento_data.get('container', equipamento.container)
                equipamento.destino = equipamento_data.get('destino', equipamento.destino)
                equipamento.save()
                if equipamentos.exists():
                    equipamentos_atualizados += 1
            
            return JsonResponse({
                "success": True,
                "mensagem": f"Sincronização concluída: {equipamentos_criados} criados, {equipamentos_atualizados} atualizados",
                "dados": {
                    "criados": equipamentos_criados,
                    "atualizados": equipamentos_atualizados
                }
            }, status=200)
            
        except json.JSONDecodeError as e:
            return JsonResponse({
                "success": False,
                "erro": f"Erro ao decodificar JSON: {str(e)}"
            }, status=400)
        except Exception as e:
            print(f"Erro na sincronização: {str(e)}")
            return JsonResponse({
                "success": False,
                "erro": f"Erro na sincronização: {str(e)}"
            }, status=500)
    
    return JsonResponse({
        "success": False,
        "erro": "Método não permitido"
    }, status=405)

def campos_banco_api(request):
    """
    Retorna um dicionário {identificador: {BL, container, destino}} de todos os equipamentos do banco.
    """
    dados = {
        str(eq.identificador): {
            "BL": eq.BL,
            "container": eq.container,
            "destino": eq.destino
        }
        for eq in Equipamento.objects.all()
    }
    return JsonResponse(dados)




