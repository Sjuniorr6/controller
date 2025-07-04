import requests
import json

# Teste da API T42
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"

def testar_api_t42():
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
        
        print("✅ API T42 conectada com sucesso!")
        print(f"📊 Total de equipamentos: {len(data)}")
        
        if data:
            primeiro_equip = data[0]
            print("\n🔍 Estrutura do primeiro equipamento:")
            print(json.dumps(primeiro_equip, indent=2, ensure_ascii=False))
            
            print("\n📋 Campos disponíveis:")
            for campo in primeiro_equip.keys():
                print(f"  - {campo}: {primeiro_equip[campo]}")
            
            # Procurar por campos relacionados a luminosidade
            campos_luz = [campo for campo in primeiro_equip.keys() if 'luz' in campo.lower() or 'light' in campo.lower() or 'lumin' in campo.lower()]
            if campos_luz:
                print(f"\n💡 Campos de luminosidade encontrados: {campos_luz}")
            else:
                print("\n❌ Nenhum campo específico de luminosidade encontrado")
                
        return data
        
    except Exception as e:
        print(f"❌ Erro ao conectar com API T42: {e}")
        return None

if __name__ == "__main__":
    testar_api_t42() 