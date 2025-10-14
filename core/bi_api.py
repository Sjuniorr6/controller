"""
API para PowerBI Dashboard
Consolida dados das APIs T42 e AssetsControls com informações locais
"""
import json
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.utils.timezone import now
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pytz

from equipamentos.models import Equipamento
from .equipament_cnfig import EQUIPMENT_GUIDS

logger = logging.getLogger(__name__)

# Configurações das APIs
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"

ASSETCONTROL_URL = "http://cloud.assetscontrols.com:8092/OpenApi/LBS"
ASSETCONTROL_TOKEN_ID = "7e88e035-285a-4f7d-8e63-8b403d04dcfa"

# Cache timeout (6 horas = 21600 segundos)
CACHE_TIMEOUT = 21600

# Timezone de Brasília
BRASILIA_TZ = pytz.timezone('America/Sao_Paulo')


def converter_para_brasilia(dt: datetime) -> str:
    """
    Converte datetime para horário de Brasília e retorna no formato dd/mm/YYYY HH:MM:SS
    """
    # Se o datetime não tem timezone, assume UTC
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)
    
    # Converte para horário de Brasília
    dt_brasilia = dt.astimezone(BRASILIA_TZ)
    
    # Retorna formatado
    return dt_brasilia.strftime('%d/%m/%Y %H:%M:%S')


def get_geocoded_address(latitude: float, longitude: float) -> Optional[str]:
    """
    Converte coordenadas em endereço usando Nominatim (OpenStreetMap)
    Com cache para evitar requisições repetidas
    """
    if not latitude or not longitude:
        return None
    
    # Cache key baseado nas coordenadas (arredondadas para 4 casas decimais)
    cache_key = f"geocode_{round(latitude, 4)}_{round(longitude, 4)}"
    cached_address = cache.get(cache_key)
    
    if cached_address:
        return cached_address
    
    try:
        geolocator = Nominatim(user_agent="bugHunter_controller")
        location = geolocator.reverse(f"{latitude}, {longitude}", timeout=3)
        if location:
            # Cache por 30 dias
            cache.set(cache_key, location.address, 2592000)
            return location.address
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        logger.warning(f"Erro no geocoding para {latitude}, {longitude}: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado no geocoding: {e}")
    
    return None


def fetch_t42_data() -> List[Dict[str, Any]]:
    """
    Busca dados da API T42
    """
    try:
        params = {
            "commandname": "get_last_transmits",
            "user": T42_USER,
            "pass": T42_PASS,
            "format": "json"
        }
        
        response = requests.get(T42_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, list):
            return data
        return []
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados T42: {e}")
        return []


def fetch_assetscontrols_data() -> List[Dict[str, Any]]:
    """
    Busca dados da API AssetsControls
    """
    try:
        guids_string = ','.join(EQUIPMENT_GUIDS)
        payload = {
            'FAction': 'QueryLBSMonitorListByFGUIDs',
            'FTokenID': ASSETCONTROL_TOKEN_ID,
            'FGUIDs': guids_string,
            'FType': 2,
        }
        
        response = requests.post(ASSETCONTROL_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('Result') == 200 and data.get('FObject'):
            return data['FObject']
        return []
        
    except Exception as e:
        logger.error(f"Erro ao buscar dados AssetsControls: {e}")
        return []


def consolidate_equipment_data(include_geocoding: bool = False) -> List[Dict[str, Any]]:
    """
    Consolida dados das APIs com informações locais
    
    Args:
        include_geocoding: Se True, faz geocoding em tempo real (lento). 
                          Se False, tenta buscar do cache mas não faz novas requisições.
    """
    logger.info("🔄 Iniciando consolidação de dados para PowerBI")
    
    # Busca dados das APIs
    t42_data = fetch_t42_data()
    assets_data = fetch_assetscontrols_data()
    
    # Busca dados locais
    equipamentos_locais = {
        eq.identificador: eq for eq in Equipamento.objects.all()
    }
    
    consolidated_data = []
    
    # Processa dados T42
    for unit in t42_data:
        unit_id = str(unit.get('unitnumber', ''))
        equipamento_local = equipamentos_locais.get(unit_id)
        
        # Coordenadas
        latitude = unit.get('latitude')
        longitude = unit.get('longitude')
        
        # Converte coordenadas para endereço
        endereco = None
        if latitude and longitude and include_geocoding:
            endereco = get_geocoded_address(float(latitude), float(longitude))
        elif latitude and longitude:
            # Apenas tenta buscar do cache, não faz nova requisição
            cache_key = f"geocode_{round(float(latitude), 4)}_{round(float(longitude), 4)}"
            endereco = cache.get(cache_key)
        
        # Data de atualização (formato brasileiro com horário de Brasília)
        data_atualizacao = unit.get('datetime_actual', '')
        if data_atualizacao and len(data_atualizacao) >= 12:
            try:
                # Parse do formato YYYYMMDDHHMM (assume UTC)
                dt = datetime.strptime(data_atualizacao[:12], '%Y%m%d%H%M')
                data_atualizacao = converter_para_brasilia(dt)
            except ValueError:
                data_atualizacao = converter_para_brasilia(now())
        else:
            data_atualizacao = converter_para_brasilia(now())
        
        consolidated_data.append({
            'id_dispositivo': unit_id,
            'nome_dispositivo': unit.get('unitname', 'Desconhecido'),
            'tipo_api': 'T42',
            'data_atualizacao': data_atualizacao,
            'latitude': latitude,
            'longitude': longitude,
            'endereco': endereco,
            'status_porta': 'Aberta' if unit.get('door') == 1 else 'Fechada',
            'bateria': unit.get('main_voltage'),
            'temperatura': unit.get('temperature'),
            'luminosidade': unit.get('light'),
            'altitude': unit.get('altitude'),
            'velocidade': unit.get('speed'),
            'direcao': unit.get('direction'),
            'instalado': unit.get('installed', False),
            'software_version': unit.get('software_version'),
            # Dados locais
            'bl': equipamento_local.BL if equipamento_local else '',
            'container': equipamento_local.container if equipamento_local else '',
            'destino': equipamento_local.destino if equipamento_local else '',
            'lacre_inn': equipamento_local.lacre_inn if equipamento_local else '',
            'lacre': equipamento_local.lacre if equipamento_local else '',
            'status_operacao': equipamento_local.status_operacao if equipamento_local else '',
            'cliente': equipamento_local.cliente if equipamento_local else '',
            'modelo': equipamento_local.modelo if equipamento_local else '',
        })
    
    # Processa dados AssetsControls
    for asset in assets_data:
        asset_id = str(asset.get('FAssetID', '') or asset.get('FVehicleName', ''))
        equipamento_local = equipamentos_locais.get(asset_id)
        
        # Coordenadas
        latitude = asset.get('FLatitude')
        longitude = asset.get('FLongitude')
        
        # Converte coordenadas para endereço
        endereco = None
        if latitude and longitude and include_geocoding:
            endereco = get_geocoded_address(float(latitude), float(longitude))
        elif latitude and longitude:
            # Apenas tenta buscar do cache, não faz nova requisição
            cache_key = f"geocode_{round(float(latitude), 4)}_{round(float(longitude), 4)}"
            endereco = cache.get(cache_key)
        
        # Data de atualização (formato brasileiro com horário de Brasília)
        data_atualizacao = asset.get('FUpdateTime', '')
        if data_atualizacao:
            try:
                # Parse do formato YYYY-MM-DD HH:MM:SS (assume UTC)
                dt = datetime.strptime(data_atualizacao, '%Y-%m-%d %H:%M:%S')
                data_atualizacao = converter_para_brasilia(dt)
            except ValueError:
                data_atualizacao = converter_para_brasilia(now())
        else:
            data_atualizacao = converter_para_brasilia(now())
        
        # Status da porta
        fdoor = asset.get('FDoor', -1)
        status_porta = 'Desconhecido'
        if fdoor == 0:
            status_porta = 'Fechada'
        elif fdoor == 1:
            status_porta = 'Aberta'
        
        # Luminosidade
        fdesc_raw = asset.get("FExpandProto", {}).get("FDesc", "")
        luminosidade = None
        if fdesc_raw:
            try:
                fdesc = json.loads(fdesc_raw)
                luminosidade = fdesc.get("fLx")
            except json.JSONDecodeError:
                pass
        
        consolidated_data.append({
            'id_dispositivo': asset_id,
            'nome_dispositivo': asset.get('FVehicleName', 'Desconhecido'),
            'tipo_api': 'AssetsControls',
            'data_atualizacao': data_atualizacao,
            'latitude': latitude,
            'longitude': longitude,
            'endereco': endereco,
            'status_porta': status_porta,
            'bateria': asset.get('FBattery'),
            'temperatura': asset.get('FTemperature'),
            'luminosidade': luminosidade,
            'altitude': asset.get('FAltitude'),
            'velocidade': asset.get('FSpeed'),
            'direcao': asset.get('FDirection'),
            'instalado': asset.get('FInstalled', False),
            'software_version': asset.get('FSoftwareVersion'),
            # Dados locais
            'bl': equipamento_local.BL if equipamento_local else '',
            'container': equipamento_local.container if equipamento_local else '',
            'destino': equipamento_local.destino if equipamento_local else '',
            'lacre_inn': equipamento_local.lacre_inn if equipamento_local else '',
            'lacre': equipamento_local.lacre if equipamento_local else '',
            'status_operacao': equipamento_local.status_operacao if equipamento_local else '',
            'cliente': equipamento_local.cliente if equipamento_local else '',
            'modelo': equipamento_local.modelo if equipamento_local else '',
        })
    
    logger.info(f"✅ Consolidação concluída: {len(consolidated_data)} equipamentos")
    return consolidated_data


@csrf_exempt
@require_GET
def bi_dashboard_api(request):
    """
    API endpoint para PowerBI
    Retorna dados consolidados de todos os equipamentos
    """
    try:
        # Verifica cache primeiro
        cache_key = 'bi_dashboard_data'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info("📋 Retornando dados do cache")
            ultima_atualizacao = cache.get('bi_dashboard_last_update')
            # Converte para formato brasileiro com horário de Brasília
            if ultima_atualizacao and 'T' in ultima_atualizacao:
                try:
                    dt = datetime.fromisoformat(ultima_atualizacao.replace('Z', '+00:00'))
                    ultima_atualizacao = converter_para_brasilia(dt)
                except:
                    ultima_atualizacao = converter_para_brasilia(now())
            return JsonResponse({
                'success': True,
                'data': cached_data,
                'total_equipamentos': len(cached_data),
                'ultima_atualizacao': ultima_atualizacao,
                'fonte': 'cache'
            })
        
        # Se não há cache, consolida dados
        logger.info("🔄 Cache não encontrado, consolidando dados...")
        consolidated_data = consolidate_equipment_data()
        
        # Salva no cache (mantém ISO no cache para compatibilidade)
        cache.set(cache_key, consolidated_data, CACHE_TIMEOUT)
        cache.set('bi_dashboard_last_update', now().isoformat(), CACHE_TIMEOUT)
        
        # Retorna com data em formato brasileiro com horário de Brasília
        return JsonResponse({
            'success': True,
            'data': consolidated_data,
            'total_equipamentos': len(consolidated_data),
            'ultima_atualizacao': converter_para_brasilia(now()),
            'fonte': 'api'
        })
        
    except Exception as e:
        logger.error(f"❌ Erro na API PowerBI: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': [],
            'total_equipamentos': 0
        }, status=500)


@csrf_exempt
@require_GET
def bi_dashboard_stats(request):
    """
    API endpoint para estatísticas do PowerBI
    Retorna resumo dos dados
    """
    try:
        # Busca dados do cache ou consolida se necessário
        cache_key = 'bi_dashboard_data'
        cached_data = cache.get(cache_key)
        
        if not cached_data:
            cached_data = consolidate_equipment_data()
            cache.set(cache_key, cached_data, CACHE_TIMEOUT)
        
        # Calcula estatísticas
        total_equipamentos = len(cached_data)
        t42_count = len([eq for eq in cached_data if eq['tipo_api'] == 'T42'])
        assets_count = len([eq for eq in cached_data if eq['tipo_api'] == 'AssetsControls'])
        
        portas_abertas = len([eq for eq in cached_data if eq['status_porta'] == 'Aberta'])
        portas_fechadas = len([eq for eq in cached_data if eq['status_porta'] == 'Fechada'])
        
        equipamentos_com_coordenadas = len([eq for eq in cached_data if eq['latitude'] and eq['longitude']])
        equipamentos_com_endereco = len([eq for eq in cached_data if eq['endereco']])
        
        # Status de operação
        status_counts = {}
        for eq in cached_data:
            status = eq['status_operacao'] or 'Não definido'
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Formata última atualização para horário de Brasília
        ultima_atualizacao = cache.get('bi_dashboard_last_update')
        if ultima_atualizacao and 'T' in ultima_atualizacao:
            try:
                dt = datetime.fromisoformat(ultima_atualizacao.replace('Z', '+00:00'))
                ultima_atualizacao = converter_para_brasilia(dt)
            except:
                ultima_atualizacao = converter_para_brasilia(now())
        
        return JsonResponse({
            'success': True,
            'estatisticas': {
                'total_equipamentos': total_equipamentos,
                't42_equipamentos': t42_count,
                'assetscontrols_equipamentos': assets_count,
                'portas_abertas': portas_abertas,
                'portas_fechadas': portas_fechadas,
                'equipamentos_com_coordenadas': equipamentos_com_coordenadas,
                'equipamentos_com_endereco': equipamentos_com_endereco,
                'status_operacao': status_counts,
                'ultima_atualizacao': ultima_atualizacao,
            }
        })
        
    except Exception as e:
        logger.error(f"❌ Erro nas estatísticas PowerBI: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_GET
def bi_dashboard_refresh(request):
    """
    Força atualização dos dados (limpa cache e reconstrói)
    ATENÇÃO: Faz geocoding completo, pode demorar vários minutos!
    """
    try:
        logger.info("🔄 Forçando atualização dos dados PowerBI (com geocoding)")
        
        # Limpa cache
        cache.delete('bi_dashboard_data')
        cache.delete('bi_dashboard_last_update')
        
        # Reconstrói dados COM geocoding (pode demorar!)
        consolidated_data = consolidate_equipment_data(include_geocoding=True)
        
        # Salva novo cache (mantém ISO no cache)
        cache.set('bi_dashboard_data', consolidated_data, CACHE_TIMEOUT)
        cache.set('bi_dashboard_last_update', now().isoformat(), CACHE_TIMEOUT)
        
        # Retorna com data em formato brasileiro com horário de Brasília
        return JsonResponse({
            'success': True,
            'message': 'Dados atualizados com sucesso',
            'total_equipamentos': len(consolidated_data),
            'ultima_atualizacao': converter_para_brasilia(now())
        })
        
    except Exception as e:
        logger.error(f"❌ Erro ao atualizar dados PowerBI: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
