import requests
import json

# Configurações da API T42
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"

def test_t42_api():
    """Testa a API T42 para ver a estrutura dos dados retornados"""
    
    print("🔍 Testando API T42...")
    
    # 1. Testar get_units
    print("\n1. Testando get_units:")
    params = {
        "commandname": "get_units",
        "user": T42_USER,
        "pass": T42_PASS,
        "format": "json"
    }
    
    try:
        response = requests.get(T42_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Tipo de resposta: {type(data)}")
        print(f"Estrutura: {type(data).__name__}")
        
        if isinstance(data, list):
            print(f"Quantidade de unidades: {len(data)}")
            if len(data) > 0:
                print(f"Primeira unidade: {data[0]}")
        elif isinstance(data, dict):
            print(f"Chaves: {list(data.keys())}")
            print(f"Conteúdo: {data}")
        else:
            print(f"Conteúdo: {data}")
            
    except Exception as e:
        print(f"Erro ao testar get_units: {e}")
    
    # 2. Testar get_last_transmit para uma unidade específica
    print("\n2. Testando get_last_transmit:")
    
    # Primeiro, vamos pegar uma unidade para testar
    try:
        response = requests.get(T42_API_URL, params=params)
        response.raise_for_status()
        units_data = response.json()
        
        if isinstance(units_data, list) and len(units_data) > 0:
            test_unit = units_data[0]
            unit_number = test_unit.get("unitnumber")
            
            if unit_number:
                print(f"Testando com unidade: {unit_number}")
                
                # Testar get_last_transmit
                transmit_params = {
                    "commandname": "get_last_transmit",
                    "user": T42_USER,
                    "pass": T42_PASS,
                    "format": "json",
                    "unitnumber": unit_number
                }
                
                response = requests.get(T42_API_URL, params=transmit_params)
                response.raise_for_status()
                transmit_data = response.json()
                
                print(f"Status: {response.status_code}")
                print(f"Tipo de resposta: {type(transmit_data)}")
                print(f"Estrutura: {type(transmit_data).__name__}")
                
                if isinstance(transmit_data, list):
                    print(f"Quantidade de transmissões: {len(transmit_data)}")
                    if len(transmit_data) > 0:
                        print(f"Primeira transmissão: {transmit_data[0]}")
                elif isinstance(transmit_data, dict):
                    print(f"Chaves: {list(transmit_data.keys())}")
                    print(f"Conteúdo: {transmit_data}")
                else:
                    print(f"Conteúdo: {transmit_data}")
        else:
            print("Nenhuma unidade encontrada para testar")
            
    except Exception as e:
        print(f"Erro ao testar get_last_transmit: {e}")
    
    # 3. Testar get_last_transmits (plural)
    print("\n3. Testando get_last_transmits:")
    params = {
        "commandname": "get_last_transmits",
        "user": T42_USER,
        "pass": T42_PASS,
        "format": "json"
    }
    
    try:
        response = requests.get(T42_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        print(f"Status: {response.status_code}")
        print(f"Tipo de resposta: {type(data)}")
        print(f"Estrutura: {type(data).__name__}")
        
        if isinstance(data, list):
            print(f"Quantidade de transmissões: {len(data)}")
            if len(data) > 0:
                print(f"Primeira transmissão: {data[0]}")
        elif isinstance(data, dict):
            print(f"Chaves: {list(data.keys())}")
            print(f"Conteúdo: {data}")
        else:
            print(f"Conteúdo: {data}")
            
    except Exception as e:
        print(f"Erro ao testar get_last_transmits: {e}")

if __name__ == "__main__":
    test_t42_api() 