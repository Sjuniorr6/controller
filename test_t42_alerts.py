#!/usr/bin/env python3
"""
Script de teste para verificar alertas de porta e luminosidade em dispositivos T42
"""

import requests
import json
from datetime import datetime

# Configurações da API T42
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"

def make_api_request(command_name, params):
    """Faz requisição para a API T42"""
    full_params = {
        "commandname": command_name,
        "user": T42_USER,
        "pass": T42_PASS,
        "format": "json",
        **params
    }
    try:
        response = requests.get(T42_API_URL, params=full_params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro na requisição {command_name}: {e}")
        return None

def test_t42_alerts():
    """Testa a funcionalidade de alertas T42"""
    print("🧪 Testando sistema de alertas T42...")
    print("=" * 50)
    
    # 1. Obter todos os equipamentos
    print("📡 Obtendo lista de equipamentos...")
    units_data = make_api_request("get_units", {})
    
    if not units_data:
        print("❌ Não foi possível obter a lista de equipamentos")
        return
    
    print(f"✅ Encontrados {len(units_data)} equipamentos")
    
    # 2. Analisar cada equipamento
    equipamentos_com_porta = []
    equipamentos_com_luz = []
    
    for unit in units_data:
        unit_number = unit.get("unitnumber")
        unit_name = unit.get("name", f"Equipamento {unit_number}")
        unit_model = unit.get("vehiclemodel", "")
        
        print(f"\n🔍 Analisando: {unit_name} ({unit_number})")
        print(f"   Modelo: {unit_model}")
        
        # Verificar se suporta porta
        supports_door = unit_model and ("TETIS" in unit_model.upper() or "WATCHLOCK" in unit_model.upper() or "KYLOS" in unit_model.upper())
        
        if supports_door:
            print("   ✅ Suporta monitoramento de porta")
            equipamentos_com_porta.append({
                'number': unit_number,
                'name': unit_name,
                'model': unit_model
            })
        else:
            print("   ❌ Não suporta monitoramento de porta")
        
        # Obter última transmissão
        last_transmit = make_api_request("get_last_transmit", {"unitnumber": unit_number})
        
        if last_transmit:
            # Verificar se é uma lista (algumas APIs retornam lista)
            if isinstance(last_transmit, list):
                if len(last_transmit) > 0:
                    last_transmit = last_transmit[0]  # Pega o primeiro item
                else:
                    print(f"   ❌ Lista vazia de transmissões")
                    continue
            
            # Verificar porta
            if supports_door:
                door_status = last_transmit.get("door")
                if door_status is not None:
                    status_text = "Aberta" if door_status == "0" else "Fechada" if door_status == "1" else f"Desconhecido ({door_status})"
                    print(f"   🚪 Status da porta: {status_text}")
                else:
                    print(f"   ⚠️  Campo 'door' não disponível")
            
            # Verificar luminosidade
            light_status = last_transmit.get("light")
            if light_status is not None:
                try:
                    light_value = int(light_status)
                    print(f"   💡 Luminosidade: {light_value}")
                    if light_value > 15:
                        print(f"   ⚠️  ALERTA: Luminosidade alta ({light_value})")
                        equipamentos_com_luz.append({
                            'number': unit_number,
                            'name': unit_name,
                            'model': unit_model,
                            'value': light_value
                        })
                except (ValueError, TypeError):
                    print(f"   ⚠️  Valor de luminosidade inválido: {light_status}")
            else:
                print(f"   ⚠️  Campo 'light' não disponível")
            
            # Última transmissão
            last_time = last_transmit.get("datetime_actual", "N/A")
            print(f"   📅 Última transmissão: {last_time}")
        else:
            print(f"   ❌ Não foi possível obter dados de transmissão")
    
    # 3. Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DO TESTE")
    print("=" * 50)
    
    print(f"\n🚪 EQUIPAMENTOS COM MONITORAMENTO DE PORTA ({len(equipamentos_com_porta)}):")
    for equip in equipamentos_com_porta:
        print(f"   • {equip['name']} ({equip['number']}) - {equip['model']}")
    
    print(f"\n💡 EQUIPAMENTOS COM LUMINOSIDADE ALTA ({len(equipamentos_com_luz)}):")
    for equip in equipamentos_com_luz:
        print(f"   • {equip['name']} ({equip['number']}) - {equip['value']} lux")
    
    print(f"\n✅ Teste concluído em {datetime.now().strftime('%H:%M:%S')}")
    
    # 4. Testar endpoint do Django (se disponível)
    print(f"\n🌐 Testando endpoint Django...")
    try:
        django_response = requests.get("http://localhost:8000/verificar-t42-door/")
        if django_response.status_code == 200:
            django_data = django_response.json()
            print(f"   ✅ Endpoint Django funcionando")
            print(f"   📊 Resposta: {django_data}")
        else:
            print(f"   ❌ Endpoint Django retornou status {django_response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro ao testar endpoint Django: {e}")

if __name__ == "__main__":
    test_t42_alerts() 