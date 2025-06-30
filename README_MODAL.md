# Funcionalidade do Modal - Salvamento no Banco de Dados

## Visão Geral

Esta funcionalidade permite salvar as alterações feitas no modal de edição diretamente no banco de dados Django. O sistema agora inclui:

1. **Atualização de campos via modal** - Salva BL, Container e Destino
2. **Sincronização automática** - Dados da API T42 são sincronizados com o banco local
3. **Feedback visual** - Mensagens de sucesso/erro para o usuário

## Como Funciona

### 1. Modal de Edição
- Clique em qualquer linha da tabela de equipamentos
- O modal abre com os dados atuais
- Edite os campos BL, Container e Destino
- Clique em "Salvar"

### 2. Processo de Salvamento
1. JavaScript captura os dados do modal
2. Faz uma requisição AJAX para `/equipamentos/api/atualizar-campos-modal/`
3. A view Django processa os dados
4. Salva no banco de dados
5. Retorna resposta de sucesso/erro
6. Atualiza a interface

### 3. Sincronização Automática
- A cada 90 segundos, os dados da API T42 são carregados
- Automaticamente sincronizados com o banco local
- Novos equipamentos são criados
- Equipamentos existentes têm suas coordenadas atualizadas

## Arquivos Modificados

### Backend (Django)
- `equipamentos/views.py` - Novas views para atualização e sincronização
- `equipamentos/urls.py` - Novas rotas para as APIs
- `equipamentos/models.py` - Modelo Equipamento (já existia)

### Frontend (JavaScript)
- `core/templates/core/mapa.html` - JavaScript atualizado para AJAX

## APIs Criadas

### 1. Atualizar Campos do Modal
```
POST /equipamentos/api/atualizar-campos-modal/
Content-Type: application/json

{
    "unitnumber": "ID_DO_EQUIPAMENTO",
    "BL": "NOVO_BL",
    "container": "NOVO_CONTAINER", 
    "destino": "NOVO_DESTINO"
}
```

**Resposta de Sucesso:**
```json
{
    "success": true,
    "mensagem": "Campos atualizados com sucesso!",
    "dados": {
        "unitnumber": "ID_DO_EQUIPAMENTO",
        "BL": "NOVO_BL",
        "container": "NOVO_CONTAINER",
        "destino": "NOVO_DESTINO"
    }
}
```

### 2. Sincronizar Dados T42
```
POST /equipamentos/api/sincronizar-t42/
Content-Type: application/json

[
    {
        "unitnumber": "T42_001",
        "latitude": -23.5505,
        "longitude": -46.6333,
        "BL": "BL_T42_001",
        "container": "CONT_T42_001",
        "destino": "São Paulo"
    }
]
```

**Resposta de Sucesso:**
```json
{
    "success": true,
    "mensagem": "Sincronização concluída: 1 criados, 0 atualizados",
    "dados": {
        "criados": 1,
        "atualizados": 0
    }
}
```

## Como Testar

### 1. Teste Manual
1. Inicie o servidor Django: `python manage.py runserver`
2. Acesse: `http://localhost:8000/mapa/`
3. Digite um ID de equipamento no campo de busca
4. Clique em uma linha da tabela
5. Edite os campos no modal
6. Clique em "Salvar"
7. Verifique se aparece a mensagem de sucesso

### 2. Teste Automatizado
Execute o script de teste:
```bash
python test_modal.py
```

### 3. Verificar no Banco de Dados
```python
# No shell do Django
python manage.py shell

from equipamentos.models import Equipamento
equipamento = Equipamento.objects.get(identificador="SEU_ID")
print(f"BL: {equipamento.BL}")
print(f"Container: {equipamento.container}")
print(f"Destino: {equipamento.destino}")
```

## Logs de Debug

As views incluem logs para debug. Verifique o console do servidor Django para:
- Dados recebidos nas requisições
- Equipamentos criados/atualizados
- Erros durante o processamento

## Tratamento de Erros

### Erros Comuns
1. **Equipamento não encontrado** - Cria um novo registro
2. **JSON inválido** - Retorna erro 400
3. **Erro de servidor** - Retorna erro 500 com detalhes

### Mensagens de Erro
- "Unitnumber é obrigatório"
- "Erro ao decodificar JSON"
- "Erro na comunicação com o servidor"

## Segurança

- CSRF desabilitado para desenvolvimento (`@csrf_exempt`)
- Validação de dados no backend
- Tratamento de exceções
- Logs para auditoria

## Próximos Passos

1. **Autenticação** - Adicionar autenticação nas APIs
2. **Validação** - Validar formatos de dados
3. **Histórico** - Manter histórico de alterações
4. **Notificações** - Sistema de notificações em tempo real 