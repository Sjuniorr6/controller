import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.test import RequestFactory
from core.views import verificar_t42_door

def test_t42_function():
    """Testa a função verificar_t42_door diretamente"""
    print("🧪 Testando função verificar_t42_door...")
    
    # Criar uma requisição mock
    factory = RequestFactory()
    request = factory.get('/verificar-t42-door/')
    
    try:
        # Chamar a função
        response = verificar_t42_door(request)
        print(f"✅ Resposta: {response.content}")
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_t42_function() 