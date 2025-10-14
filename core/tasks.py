from __future__ import annotations

import json
import logging
import os
import requests
from typing import List, Dict, Any
from datetime import timedelta

from celery import shared_task
from django.db.models import Max
from django.utils.timezone import now
from django.core.cache import cache

from core.models import EventoTratado

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
#  CONFIGURAÇÃO
# ---------------------------------------------------------------------------
ASSETCONTROL_URL      = "http://cloud.assetscontrols.com:8092/OpenApi/LBS"
ASSETCONTROL_TOKEN_ID = "7e88e035-285a-4f7d-8e63-8b403d04dcfa"

CONFIG_FILE = os.path.join(
    os.path.dirname(__file__),
    "equipament_config.json",
)
TIMEOUT_S   = 30                     # timeout HTTP da API
LUX_LIMITE  = 15.0                   # acima disso é "luz alta"
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
#  UTILITÁRIOS
# ---------------------------------------------------------------------------
def _carregar_guids() -> List[str]:
    """Lê o equipament_config.json e devolve a lista de GUIDs a consultar."""
    try:
        with open(CONFIG_FILE, encoding="utf-8") as fp:
            cfg = json.load(fp)
        guids = cfg.get("EQUIPMENT_GUIDS", [])
        if not guids:
            logger.warning("⚠️ Nenhum GUID encontrado em %s", CONFIG_FILE)
        return guids
    except Exception as exc:
        logger.error("❌ Erro lendo %s: %s", CONFIG_FILE, exc)
        return []


def consultar_assetcontrol_equipamentos() -> List[Dict[str, Any]]:
    """Retorna lista de dicts com {id, nome, FDoor, fLx}."""
    guids = _carregar_guids()
    if not guids:
        return []

    payload = {
        "FAction": "QueryLBSMonitorListByFGUIDs",
        "FTokenID": ASSETCONTROL_TOKEN_ID,
        "FGUIDs": ",".join(guids),
        "FDateType": 2,
    }

    try:
        resp = requests.post(ASSETCONTROL_URL, json=payload, timeout=TIMEOUT_S)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.error("❌ Erro consumindo AssetControl: %s", exc)
        return []

    if data.get("Result") != 200 or not data.get("FObject"):
        logger.warning("⚠️ Resposta vazia/inesperada da AssetControl.")
        return []

    resultados: List[Dict[str, Any]] = []
    for obj in data["FObject"]:
        guid = obj.get("FAssetID")
        nome = obj.get("FVehicleName") or "Desconhecido"
        porta = int(obj.get("FDoor", -1))

        raw_desc = obj.get("FExpandProto", {}).get("FDesc", "")
        try:
            desc = json.loads(raw_desc) if raw_desc else {}
            luz = float(desc.get("fLx", -1))
        except Exception:
            luz = -1

        resultados.append({
            "id": guid,
            "nome": nome,
            "FDoor": porta,
            "fLx": luz,
        })

    return resultados


# ---------------------------------------------------------------------------
#  TASK CELERY SEM COOLDOWN E COM DEBUG
# ---------------------------------------------------------------------------
@shared_task
def verificar_alertas_equipamentos() -> None:
    """
    * Consulta a API.
    * Compara com o último valor salvo no BD.
    * Dispara alerta imediato a cada mudança e salva no BD.
    """
    logger.warning("🔁 Verificando AssetControl…")

    resultados = consultar_assetcontrol_equipamentos()
    if not resultados:
        return

    # 1) carrega último estado do BD
    sub = (
        EventoTratado.objects
        .values("guid", "tipo_evento")
        .annotate(ultimo_id=Max("id"))
    )
    ultimos = EventoTratado.objects.filter(
        id__in=[u["ultimo_id"] for u in sub]
    ).values("guid", "tipo_evento", "valor")

    estado_cache = {
        (u["guid"], u["tipo_evento"]): u["valor"]
        for u in ultimos
    }

    novos_eventos: list[EventoTratado] = []

    # 2) percorre resultados e alerta sempre que houver mudança
    for r in resultados:
        guid, nome = r["id"], r["nome"]

        # Porta
        if r["FDoor"] in (0, 1):
            key = (guid, "door")
            antigo = estado_cache.get(key)
            novo = r["FDoor"]
            logger.debug("DEBUG %s → FDoor=%s (antes=%s)", guid, novo, antigo)
            if antigo != novo:
                estado_cache[key] = novo
                logger.warning(
                    "🚪 Porta %s – %s (%s)",
                    "aberta" if novo else "fechada",
                    nome,
                    guid,
                )
                novos_eventos.append(
                    EventoTratado(
                        guid=guid,
                        tipo_evento="door",
                        valor=novo,
                        criado_em=now(),
                    )
                )

        # Luz
        if r["fLx"] >= 0:
            key = (guid, "light")
            antigo = estado_cache.get(key)
            novo = r["fLx"]
            logger.debug("DEBUG %s → fLx=%.1f (antes=%s)", guid, novo, antigo)
            if antigo != novo:
                estado_cache[key] = novo
                if novo > LUX_LIMITE:
                    logger.warning(
                        "💡 Luz alta (%.1f) em %s (%s)",
                        novo, nome, guid
                    )
                else:
                    logger.warning(
                        "💡 Luz mudou para %.1f em %s (%s)",
                        novo, nome, guid
                    )
                novos_eventos.append(
                    EventoTratado(
                        guid=guid,
                        tipo_evento="light",
                        valor=novo,
                        criado_em=now(),
                    )
                )

    # 3) salva novos eventos em lote
    if novos_eventos:
        EventoTratado.objects.bulk_create(novos_eventos, batch_size=500)
        logger.info("💾 %d novos eventos gravados", len(novos_eventos))
    else:
        logger.debug("🔍 Nenhuma mudança — nada gravado")


# ---------------------------------------------------------------------------
#  TASK PARA ATUALIZAR DADOS DO POWERBI
# ---------------------------------------------------------------------------
@shared_task
def atualizar_dados_powerbi() -> None:
    """
    Atualiza os dados do PowerBI 4 vezes ao dia (a cada 6 horas)
    Consolida dados das APIs T42 e AssetsControls COM geocoding
    """
    logger.info("🔄 Iniciando atualização dos dados PowerBI (com geocoding)")
    
    try:
        # Importa aqui para evitar import circular
        from .bi_api import consolidate_equipment_data
        
        # Consolida dados COM geocoding (pode demorar)
        consolidated_data = consolidate_equipment_data(include_geocoding=True)
        
        # Salva no cache
        cache.set('bi_dashboard_data', consolidated_data, 21600)  # 6 horas
        cache.set('bi_dashboard_last_update', now().isoformat(), 21600)
        
        logger.info("✅ Dados PowerBI atualizados com sucesso: %d equipamentos", len(consolidated_data))
        
    except Exception as e:
        logger.error("❌ Erro ao atualizar dados PowerBI: %s", str(e))


# ---------------------------------------------------------------------------
#  TASK PARA VERIFICAR GEOFENCING (SAÍDA DE FAZENDA E PARADO NO PORTO)
# ---------------------------------------------------------------------------
@shared_task
def verificar_geofencing_equipamentos() -> None:
    """
    Verifica geofencing de todos os equipamentos:
    - Detecta saídas de fazendas
    - Detecta equipamentos parados no porto por mais de 10 dias
    """
    logger.info("🗺️ Iniciando verificação de geofencing")
    
    try:
        from .geofencing_manager import processar_equipamento
        
        # Busca dados das APIs
        equipamentos_processados = 0
        alertas_criados = 0
        
        # Processa T42
        try:
            params = {
                "commandname": "get_last_transmits",
                "user": "wimc_u_nestle",
                "pass": "Inte@20xx",
                "format": "json"
            }
            
            response = requests.get(
                "https://mongol.brono.com/mongol/api.php",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            t42_data = response.json()
            
            if isinstance(t42_data, list):
                for unit in t42_data:
                    guid = str(unit.get('unitnumber', ''))
                    nome = unit.get('unitname', 'Desconhecido')
                    lat = unit.get('latitude')
                    lng = unit.get('longitude')
                    velocidade = unit.get('speed')
                    
                    if lat and lng:
                        try:
                            processar_equipamento(guid, nome, float(lat), float(lng), velocidade)
                            equipamentos_processados += 1
                        except Exception as e:
                            logger.error(f"Erro processando {guid}: {e}")
                            
        except Exception as e:
            logger.error(f"Erro ao buscar dados T42: {e}")
        
        # Processa AssetsControls
        try:
            guids = _carregar_guids()
            if guids:
                payload = {
                    "FAction": "QueryLBSMonitorListByFGUIDs",
                    "FTokenID": ASSETCONTROL_TOKEN_ID,
                    "FGUIDs": ",".join(guids),
                    "FDateType": 2,
                }
                
                response = requests.post(ASSETCONTROL_URL, json=payload, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                if data.get("Result") == 200 and data.get("FObject"):
                    for obj in data["FObject"]:
                        guid = obj.get("FAssetID")
                        nome = obj.get("FVehicleName", "Desconhecido")
                        lat = obj.get("FLatitude")
                        lng = obj.get("FLongitude")
                        velocidade = obj.get("FSpeed")
                        
                        if guid and lat and lng:
                            try:
                                processar_equipamento(guid, nome, float(lat), float(lng), velocidade)
                                equipamentos_processados += 1
                            except Exception as e:
                                logger.error(f"Erro processando {guid}: {e}")
                                
        except Exception as e:
            logger.error(f"Erro ao buscar dados AssetsControls: {e}")
        
        # Estatísticas
        from .geofencing_manager import obter_alertas_ativos
        estatisticas = obter_alertas_ativos()
        
        logger.info(
            f"✅ Geofencing verificado: {equipamentos_processados} equipamentos processados | "
            f"{estatisticas['total']} alertas ativos "
            f"({estatisticas['saidas_fazenda']} saídas, {estatisticas['parados_porto']} parados)"
        )
        
    except Exception as e:
        logger.error(f"❌ Erro ao verificar geofencing: {e}")
