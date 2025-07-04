import requests
import json
from datetime import datetime, timedelta

# --- Configurações da API ---
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx" # SUBSTITUA PELA SUA SENHA REAL

# --- Função para fazer requisições GET à API ---
def make_api_request(command_name, params ):
    full_params = {
        "commandname": command_name,
        "user": T42_USER,
        "pass": T42_PASS,
        "format": "json1",
        **params # Adiciona os parâmetros específicos do comando
    }
    try:
        response = requests.get(T42_API_URL, params=full_params)
        response.raise_for_status() # Levanta um erro para status HTTP 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição {command_name}: {e}")
        if response:
            print(f"Resposta da API: {response.text}")
        return None

# --- 1. Obter todos os equipamentos ---
print("Obtendo lista de todos os equipamentos...")
units_data = make_api_request("get_units", {})

if units_data:
    print(f"Total de equipamentos encontrados: {len(units_data)}")
    all_units_door_status = {}

    for unit in units_data:
        unit_number = unit.get("unitnumber")
        unit_name = unit.get("name")
        unit_model = unit.get("vehiclemodel") # Importante para verificar o tipo

        print(f"\nProcessando unidade: {unit_name} ({unit_number}) - Modelo: {unit_model}")

        # --- 2. Para cada equipamento, obter o estado da porta (última transmissão) ---
        # Usamos get_last_transmit para o estado atual, que é mais eficiente
        last_transmit_data = make_api_request("get_last_transmit", {"unitnumber": unit_number})

        if last_transmit_data:
            # A resposta de get_last_transmit é um único objeto JSON, não uma lista
            # O campo 'door' só é relevante para modelos Tetis, Watchlock, Kylos
            door_status_code = last_transmit_data.get("door")
            
            status_text = "N/A (Campo 'door' não disponível ou modelo incompatível)"
            if unit_model and ("Tetis" in unit_model or "Watchlock" in unit_model or "Kylos" in unit_model):
                if door_status_code == "0":
                    status_text = "Aberta"
                elif door_status_code == "1":
                    status_text = "Fechada"
                else:
                    status_text = f"Desconhecido ({door_status_code})"
            
            all_units_door_status[unit_number] = {
                "name": unit_name,
                "model": unit_model,
                "door_status": status_text,
                "last_transmit_time": last_transmit_data.get("datetime_actual")
            }
            print(f"  Status da Porta: {status_text}")
        else:
            print(f"  Não foi possível obter a última transmissão para {unit_number}.")
            all_units_door_status[unit_number] = {
                "name": unit_name,
                "model": unit_model,
                "door_status": "Não disponível (Erro na requisição)",
                "last_transmit_time": "N/A"
            }
else:
    print("Não foi possível obter a lista de equipamentos.")

# --- Exibir o resumo final ---
print("\n--- Resumo do Status das Portas de Todos os Equipamentos ---")
for unit_num, info in all_units_door_status.items():
    print(f"Unidade {unit_num} ({info['name']}) - Modelo: {info['model']}: Porta {info['door_status']} (Última Transmissão: {info['last_transmit_time']})")