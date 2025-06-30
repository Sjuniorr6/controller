#!/usr/bin/env python3
"""
Script de teste para verificar a funcionalidade do modal
"""
import requests
import json

# URL base do servidor Django
BASE_URL = "http://localhost:8000"

def test_atualizar_campos_modal():
    """Testa a atualização de campos via modal"""
    
    # Dados de teste
    dados_teste = {
        "unitnumber": "TEST001",
        "BL": "BL123456",
        "container": "CONT789",
        "destino": "São Paulo"
    }
    
    print("Testando atualização de campos via modal...")
    print(f"Dados de teste: {dados_teste}")
    
    try:
        # Faz a requisição POST
        response = requests.post(
            f"{BASE_URL}/equipamentos/api/atualizar-campos-modal/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(dados_teste)
        )
        
        print(f"Status da resposta: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Teste PASSOU - Campos atualizados com sucesso!")
                return True
            else:
                print(f"❌ Teste FALHOU - Erro: {data.get('erro')}")
                return False
        else:
            print(f"❌ Teste FALHOU - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

def test_sincronizar_t42():
    """Testa a sincronização de dados T42"""
    
    # Dados de teste simulando API T42
    dados_t42 = [
        {
            "unitnumber": "T42_001",
            "latitude": -23.5505,
            "longitude": -46.6333,
            "BL": "BL_T42_001",
            "container": "CONT_T42_001",
            "destino": "Rio de Janeiro"
        },
        {
            "unitnumber": "T42_002",
            "latitude": -21.6319,
            "longitude": -45.2740,
            "BL": "BL_T42_002",
            "container": "CONT_T42_002",
            "destino": "Minas Gerais"
        }
    ]
    
    print("\nTestando sincronização de dados T42...")
    print(f"Dados de teste: {len(dados_t42)} equipamentos")
    
    try:
        # Faz a requisição POST
        response = requests.post(
            f"{BASE_URL}/equipamentos/api/sincronizar-t42/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(dados_t42)
        )
        
        print(f"Status da resposta: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Teste PASSOU - Sincronização realizada com sucesso!")
                return True
            else:
                print(f"❌ Teste FALHOU - Erro: {data.get('erro')}")
                return False
        else:
            print(f"❌ Teste FALHOU - Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== TESTE DA FUNCIONALIDADE DO MODAL ===\n")
    
    # Testa atualização de campos
    test1_passed = test_atualizar_campos_modal()
    
    # Testa sincronização T42
    test2_passed = test_sincronizar_t42()
    
    print("\n=== RESULTADO DOS TESTES ===")
    print(f"Teste 1 (Atualizar campos): {'✅ PASSOU' if test1_passed else '❌ FALHOU'}")
    print(f"Teste 2 (Sincronizar T42): {'✅ PASSOU' if test2_passed else '❌ FALHOU'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM!") 