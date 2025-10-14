"""
Gerenciador de Geofencing e Alertas
Detecta saídas de fazendas e equipamentos parados em portos
"""
import logging
from math import radians, cos, sin, asin, sqrt
from datetime import timedelta
from django.utils.timezone import now
from typing import Optional, Dict, Any

from .models import PosicaoEquipamento, AlertaGeofencing
from .geofences import GEOFENCES, TIPO_FAZENDA, TIPO_PORTO

logger = logging.getLogger(__name__)

# Configurações
DIAS_LIMITE_PORTO = 10  # Dias parados no porto para gerar alerta


def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula distância entre dois pontos em metros usando fórmula de Haversine
    """
    # Converte para radianos
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Fórmula de Haversine
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Raio da Terra em metros
    r = 6371000
    return c * r


def verificar_geofence(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    """
    Verifica se uma posição está dentro de alguma geofence
    Retorna informações da cerca se estiver dentro, None caso contrário
    """
    for geofence in GEOFENCES:
        distancia = calcular_distancia(
            latitude, longitude,
            geofence['lat'], geofence['lng']
        )
        
        if distancia <= geofence['raio_m']:
            return {
                'nome': geofence['nome'],
                'tipo': geofence['tipo'],
                'distancia': distancia,
                'raio': geofence['raio_m']
            }
    
    return None


def registrar_posicao(guid: str, nome_equipamento: str, latitude: float, 
                     longitude: float, velocidade: Optional[float] = None) -> PosicaoEquipamento:
    """
    Registra uma nova posição do equipamento e verifica geofencing
    """
    # Verifica se está em alguma cerca
    cerca_info = verificar_geofence(latitude, longitude)
    
    # Cria registro de posição
    posicao = PosicaoEquipamento.objects.create(
        guid=guid,
        nome_equipamento=nome_equipamento,
        latitude=latitude,
        longitude=longitude,
        velocidade=velocidade,
        parado=(velocidade == 0 if velocidade is not None else False),
        dentro_de_cerca=cerca_info is not None,
        nome_cerca=cerca_info['nome'] if cerca_info else None,
        tipo_cerca=cerca_info['tipo'] if cerca_info else None,
    )
    
    logger.debug(
        f"📍 Posição registrada: {nome_equipamento} - "
        f"{'Dentro de ' + cerca_info['nome'] if cerca_info else 'Fora de cercas'}"
    )
    
    return posicao


def verificar_saida_fazenda(guid: str, nome_equipamento: str, 
                            posicao_atual: PosicaoEquipamento) -> None:
    """
    Verifica se o equipamento saiu de uma fazenda
    Compara posição atual com a última posição registrada
    """
    # Busca posição anterior
    posicao_anterior = PosicaoEquipamento.objects.filter(
        guid=guid
    ).exclude(id=posicao_atual.id).first()
    
    if not posicao_anterior:
        return  # Primeira posição registrada, nada a comparar
    
    # Verifica se saiu de uma fazenda
    if (posicao_anterior.dentro_de_cerca and 
        posicao_anterior.tipo_cerca == TIPO_FAZENDA and
        not posicao_atual.dentro_de_cerca):
        
        # Verifica se já existe alerta recente (últimas 24h)
        alerta_recente = AlertaGeofencing.objects.filter(
            guid=guid,
            tipo_alerta=AlertaGeofencing.TIPO_SAIDA_FAZENDA,
            criado_em__gte=now() - timedelta(hours=24),
            resolvido=False
        ).exists()
        
        if not alerta_recente:
            # Cria alerta de saída
            alerta = AlertaGeofencing.objects.create(
                guid=guid,
                nome_equipamento=nome_equipamento,
                tipo_alerta=AlertaGeofencing.TIPO_SAIDA_FAZENDA,
                nome_local=posicao_anterior.nome_cerca,
                latitude=posicao_atual.latitude,
                longitude=posicao_atual.longitude,
                saiu_em=now(),
                alerta_disparado=False
            )
            
            logger.warning(
                f"🚨 ALERTA: {nome_equipamento} SAIU da fazenda {posicao_anterior.nome_cerca}!"
            )
            
            return alerta


def verificar_equipamento_parado_porto(guid: str, nome_equipamento: str) -> None:
    """
    Verifica se equipamento está parado no porto por mais de 10 dias
    """
    # Busca posições no porto nos últimos 15 dias
    data_limite = now() - timedelta(days=15)
    
    posicoes_porto = PosicaoEquipamento.objects.filter(
        guid=guid,
        dentro_de_cerca=True,
        tipo_cerca=TIPO_PORTO,
        timestamp__gte=data_limite
    ).order_by('timestamp')
    
    if not posicoes_porto.exists():
        return  # Não está em nenhum porto
    
    # Pega primeira e última posição no porto
    primeira_posicao = posicoes_porto.first()
    ultima_posicao = posicoes_porto.last()
    
    # Verifica se é o mesmo porto
    if primeira_posicao.nome_cerca != ultima_posicao.nome_cerca:
        return  # Mudou de porto, não está parado
    
    # Calcula dias parado
    tempo_parado = now() - primeira_posicao.timestamp
    dias_parado = tempo_parado.days
    
    # Verifica se passou do limite
    if dias_parado >= DIAS_LIMITE_PORTO:
        # Verifica se já existe alerta ativo
        alerta_existente = AlertaGeofencing.objects.filter(
            guid=guid,
            tipo_alerta=AlertaGeofencing.TIPO_PARADO_PORTO,
            nome_local=ultima_posicao.nome_cerca,
            resolvido=False
        ).first()
        
        if alerta_existente:
            # Atualiza dias parado
            alerta_existente.dias_parado = dias_parado
            alerta_existente.save()
            
            logger.info(
                f"⏰ Alerta atualizado: {nome_equipamento} parado há {dias_parado} dias "
                f"no {ultima_posicao.nome_cerca}"
            )
        else:
            # Cria novo alerta
            alerta = AlertaGeofencing.objects.create(
                guid=guid,
                nome_equipamento=nome_equipamento,
                tipo_alerta=AlertaGeofencing.TIPO_PARADO_PORTO,
                nome_local=ultima_posicao.nome_cerca,
                latitude=ultima_posicao.latitude,
                longitude=ultima_posicao.longitude,
                parado_desde=primeira_posicao.timestamp,
                dias_parado=dias_parado,
                alerta_disparado=False
            )
            
            logger.warning(
                f"🚨 ALERTA: {nome_equipamento} PARADO há {dias_parado} dias "
                f"no {ultima_posicao.nome_cerca}!"
            )
            
            return alerta


def resolver_alertas_automaticamente(guid: str) -> None:
    """
    Resolve alertas automaticamente quando:
    - Equipamento saiu do porto (resolve alerta de parado)
    - Equipamento voltou para fazenda (resolve alerta de saída)
    """
    # Busca posição atual
    posicao_atual = PosicaoEquipamento.objects.filter(guid=guid).first()
    
    if not posicao_atual:
        return
    
    # Resolve alertas de saída de fazenda se voltou para uma fazenda
    if posicao_atual.dentro_de_cerca and posicao_atual.tipo_cerca == TIPO_FAZENDA:
        alertas_saida = AlertaGeofencing.objects.filter(
            guid=guid,
            tipo_alerta=AlertaGeofencing.TIPO_SAIDA_FAZENDA,
            resolvido=False
        )
        
        for alerta in alertas_saida:
            alerta.resolver()
            logger.info(
                f"✅ Alerta resolvido: {alerta.nome_equipamento} voltou para fazenda"
            )
    
    # Resolve alertas de parado no porto se saiu do porto
    if not posicao_atual.dentro_de_cerca or posicao_atual.tipo_cerca != TIPO_PORTO:
        alertas_porto = AlertaGeofencing.objects.filter(
            guid=guid,
            tipo_alerta=AlertaGeofencing.TIPO_PARADO_PORTO,
            resolvido=False
        )
        
        for alerta in alertas_porto:
            alerta.resolver()
            logger.info(
                f"✅ Alerta resolvido: {alerta.nome_equipamento} saiu do porto"
            )


def processar_equipamento(guid: str, nome_equipamento: str, latitude: float,
                         longitude: float, velocidade: Optional[float] = None) -> None:
    """
    Função principal que processa um equipamento:
    1. Registra posição
    2. Verifica saída de fazenda
    3. Verifica equipamento parado no porto
    4. Resolve alertas automaticamente
    """
    # Registra posição
    posicao = registrar_posicao(guid, nome_equipamento, latitude, longitude, velocidade)
    
    # Verifica saída de fazenda
    verificar_saida_fazenda(guid, nome_equipamento, posicao)
    
    # Verifica equipamento parado no porto
    verificar_equipamento_parado_porto(guid, nome_equipamento)
    
    # Resolve alertas automaticamente
    resolver_alertas_automaticamente(guid)


def obter_alertas_ativos() -> Dict[str, Any]:
    """
    Retorna estatísticas dos alertas ativos
    """
    alertas_saida = AlertaGeofencing.objects.filter(
        tipo_alerta=AlertaGeofencing.TIPO_SAIDA_FAZENDA,
        resolvido=False,
        status='pendente'
    ).count()
    
    alertas_porto = AlertaGeofencing.objects.filter(
        tipo_alerta=AlertaGeofencing.TIPO_PARADO_PORTO,
        resolvido=False,
        status='pendente'
    ).count()
    
    return {
        'total': alertas_saida + alertas_porto,
        'saidas_fazenda': alertas_saida,
        'parados_porto': alertas_porto,
    }

