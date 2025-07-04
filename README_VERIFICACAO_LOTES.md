# Verificação de Porta e Luminosidade em Lote

Este documento descreve as novas funcionalidades implementadas para verificação de status de porta e luminosidade em lote, utilizando os lotes de equipamentos definidos no arquivo `equipament_cnfig.py`.

## Funcionalidades Implementadas

### 1. Verificação Geral em Lote
**Endpoint:** `GET /verificar-fdoor/`

Verifica todos os equipamentos de todos os lotes ou de um lote específico.

**Parâmetros:**
- `lote` (opcional): ID do lote específico (ex: `lote_1`, `lote_2`, etc.)

**Exemplos de uso:**
```bash
# Verificar todos os equipamentos de todos os lotes
GET /verificar-fdoor/

# Verificar apenas equipamentos do lote 1
GET /verificar-fdoor/?lote=lote_1

# Verificar apenas equipamentos do lote 3
GET /verificar-fdoor/?lote=lote_3
```

**Resposta de sucesso:**
```json
{
    "eventos": [
        {
            "evento": "aberta",
            "equipamento": "Equipamento XYZ",
            "guid": "f0d11885-b7db-4565-a7d1-14f3e8faa362",
            "lote": "Lote 6 - Equipamentos de Transporte"
        },
        {
            "evento": "luz",
            "equipamento": "Equipamento ABC",
            "guid": "b6f21817-a416-49de-9ce2-15954ec83b33",
            "valor": 25.5,
            "lote": "Lote 6 - Equipamentos de Transporte"
        }
    ],
    "total_eventos": 2,
    "lote_consultado": "Lote 6 - Equipamentos de Transporte",
    "total_equipamentos": 10
}
```

**Resposta sem eventos:**
```json
{
    "eventos": [],
    "total_eventos": 0,
    "lote_consultado": "Todos os lotes",
    "total_equipamentos": 100,
    "mensagem": "Nenhum evento detectado"
}
```

### 2. Verificação de Lote Específico
**Endpoint:** `GET /verificar-fdoor/lote/{lote_id}/`

Verifica equipamentos de um lote específico usando o ID do lote na URL.

**Exemplos de uso:**
```bash
# Verificar lote 1
GET /verificar-fdoor/lote/lote_1/

# Verificar lote 5
GET /verificar-fdoor/lote/lote_5/
```

### 3. Listagem de Lotes Disponíveis
**Endpoint:** `GET /lotes/`

Retorna informações sobre todos os lotes disponíveis.

**Resposta:**
```json
{
    "lotes": [
        {
            "id": "lote_1",
            "nome": "Lote 1 - Equipamentos Principais",
            "total_equipamentos": 10
        },
        {
            "id": "lote_2",
            "nome": "Lote 2 - Equipamentos Secundários",
            "total_equipamentos": 10
        }
    ],
    "total_lotes": 10
}
```

## Tipos de Eventos Detectados

### 1. Porta Aberta
- **Condição:** Status da porta mudou de fechada (0) para aberta (1)
- **Resposta:** `"evento": "aberta"`

### 2. Porta Fechada
- **Condição:** Status da porta mudou de aberta (1) para fechada (0)
- **Resposta:** `"evento": "fechada"`

### 3. Alerta de Luminosidade
- **Condição:** Valor de luminosidade (fLx) > 15 e não foi alertado recentemente
- **Resposta:** `"evento": "luz"` com valor da luminosidade

## Lotes Disponíveis

Os equipamentos estão organizados em 10 lotes:

1. **lote_1**: Lote 1 - Equipamentos Principais (10 equipamentos)
2. **lote_2**: Lote 2 - Equipamentos Secundários (10 equipamentos)
3. **lote_3**: Lote 3 - Equipamentos de Monitoramento (10 equipamentos)
4. **lote_4**: Lote 4 - Equipamentos de Controle (10 equipamentos)
5. **lote_5**: Lote 5 - Equipamentos de Logística (10 equipamentos)
6. **lote_6**: Lote 6 - Equipamentos de Transporte (10 equipamentos)
7. **lote_7**: Lote 7 - Equipamentos de Armazenamento (10 equipamentos)
8. **lote_8**: Lote 8 - Equipamentos de Distribuição (10 equipamentos)
9. **lote_9**: Lote 9 - Equipamentos de Produção (10 equipamentos)
10. **lote_10**: Lote 10 - Equipamentos de Qualidade (10 equipamentos)

## Cache e Controle de Estado

O sistema utiliza cache para controlar:
- **Status anterior da porta:** Evita alertas duplicados
- **Alertas de luminosidade:** Evita spam de alertas (timeout de 1 hora)

## Tratamento de Erros

### Lote não encontrado
```json
{
    "error": "Lote lote_invalido não encontrado"
}
```

### Erro na API
```json
{
    "error": "Erro ao consultar a API: Connection timeout",
    "lote_consultado": "Lote 1 - Equipamentos Principais"
}
```

## Exemplos de Integração

### JavaScript/Frontend
```javascript
// Verificar todos os equipamentos
fetch('/verificar-fdoor/')
    .then(response => response.json())
    .then(data => {
        if (data.eventos.length > 0) {
            data.eventos.forEach(evento => {
                console.log(`Evento: ${evento.evento} - Equipamento: ${evento.equipamento}`);
            });
        }
    });

// Verificar lote específico
fetch('/verificar-fdoor/?lote=lote_1')
    .then(response => response.json())
    .then(data => {
        console.log(`Total de eventos: ${data.total_eventos}`);
    });

// Listar lotes disponíveis
fetch('/lotes/')
    .then(response => response.json())
    .then(data => {
        data.lotes.forEach(lote => {
            console.log(`${lote.nome}: ${lote.total_equipamentos} equipamentos`);
        });
    });
```

### Python/Backend
```python
import requests

# Verificar lote específico
response = requests.get('http://localhost:8000/verificar-fdoor/?lote=lote_1')
data = response.json()

if data['total_eventos'] > 0:
    for evento in data['eventos']:
        print(f"Evento detectado: {evento['evento']} em {evento['equipamento']}")
```

## Monitoramento Contínuo

Para monitoramento contínuo, recomenda-se:
1. Fazer chamadas periódicas (ex: a cada 30 segundos)
2. Implementar retry em caso de falhas
3. Logar eventos importantes para auditoria
4. Configurar alertas para eventos críticos

## Performance

- **Consulta completa:** ~100 equipamentos por requisição
- **Consulta por lote:** ~10 equipamentos por requisição
- **Cache:** 1 hora para evitar spam de alertas
- **Timeout:** Configurado para evitar travamentos 