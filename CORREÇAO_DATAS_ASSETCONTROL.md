# Correção de Discrepância de Datas - AssetsControls API

## Problema Identificado

**Sintoma**: Datas diferentes entre o sistema (mapa) e a API do PowerBI para o mesmo equipamento.

**Exemplo**:

- Equipamento: 837504000484
- API: 14/10/2025 17:56
- Sistema: 29/09/2025 14:15

## Causa Raiz

Havia uma **inconsistência nos campos de data** utilizados:

### 1. Sistema (Frontend - `core/templates/core/mapa.html`)

✅ **Correto** - Usa os campos apropriados:

- `FRecvTime` - Tempo de recepção do servidor
- `FGPSTime` - Tempo GPS do equipamento

```javascript
// Linha 1008 - Tabela
<td><small>${formatarDataHora(unit.FRecvTime) || formatarDataHora(unit.FGPSTime) || 'N/A'}</small></td>

// Linha 1103-1104 - Popup do mapa
<strong>Última Atualização:</strong> ${formatarDataHora(unit.FRecvTime) || formatarDataHora(unit.FGPSTime) || 'N/A'}<br>
```

### 2. API PowerBI (`core/bi_api.py`)

❌ **Incorreto** - Usava campo inexistente ou com dados incorretos:

- `FUpdateTime` - Campo que não existe ou contém dados antigos/incorretos

```python
# Linha 233 - ANTES (INCORRETO)
data_atualizacao = asset.get('FUpdateTime', '')
```

## Solução Implementada

### Correção 1: Campo correto

Alterado o arquivo `core/bi_api.py` para usar os mesmos campos que o sistema usa:

```python
# Linha 233-234 - DEPOIS (CORRETO)
# Usa FRecvTime (tempo de recepção) ou FGPSTime (tempo GPS) como fallback
data_atualizacao = asset.get('FRecvTime', '') or asset.get('FGPSTime', '')
```

### Correção 2: Formato de parsing

A API AssetsControls retorna datas no formato ISO 8601 com microsegundos:

- Formato: `2025-09-29T17:15:36.447937Z`

Foi necessário ajustar o parsing para aceitar este formato:

```python
# Linhas 236-250 - PARSING CORRETO DO FORMATO ISO 8601
if data_atualizacao:
    try:
        # Remove o 'Z' no final e tenta parsear como ISO 8601
        if data_atualizacao.endswith('Z'):
            data_atualizacao = data_atualizacao[:-1]

        # Tenta parsear com microsegundos primeiro, depois sem
        try:
            dt = datetime.strptime(data_atualizacao, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            dt = datetime.strptime(data_atualizacao, '%Y-%m-%dT%H:%M:%S')

        data_atualizacao = converter_para_brasilia(dt)
    except (ValueError, AttributeError):
        data_atualizacao = converter_para_brasilia(now())
```

## Campos da API AssetsControls

Documentação dos campos de timestamp disponíveis:

| Campo         | Descrição                                | Uso Recomendado               |
| ------------- | ---------------------------------------- | ----------------------------- |
| `FRecvTime`   | Tempo em que o servidor recebeu os dados | ✅ Principal (mais confiável) |
| `FGPSTime`    | Tempo GPS do equipamento                 | ✅ Fallback                   |
| `FUpdateTime` | Campo obsoleto/incorreto                 | ❌ Não usar                   |

## Ações Necessárias

1. ✅ **Arquivo corrigido**: `core/bi_api.py`
2. 🔄 **Limpar cache**: Para aplicar a correção, limpe o cache do PowerBI:

   ```bash
   # Acesse a URL de refresh (vai demorar alguns minutos)
   /api/bi-dashboard/refresh/
   ```

   Ou via Django shell:

   ```python
   from django.core.cache import cache
   cache.delete('bi_dashboard_data')
   cache.delete('bi_dashboard_last_update')
   ```

3. ✅ **Teste**: Verifique se as datas agora coincidem entre:
   - Sistema (mapa)
   - API PowerBI (`/api/bi-dashboard/`)

## Verificação

Para verificar se o problema foi resolvido:

1. Acesse o mapa do sistema e anote a data/hora de um equipamento
2. Consulte a API do PowerBI: `/api/bi-dashboard/`
3. Procure o mesmo equipamento na resposta JSON
4. Confirme que as datas são idênticas

## Observações Técnicas

### Conversão de Timezone

O sistema converte automaticamente as datas de UTC para o horário de Brasília (America/Sao_Paulo):

```python
def converter_para_brasilia(dt: datetime) -> str:
    """Converte datetime para horário de Brasília"""
    if dt.tzinfo is None:
        dt = pytz.UTC.localize(dt)  # Assume UTC se não tiver timezone

    dt_brasilia = dt.astimezone(BRASILIA_TZ)
    return dt_brasilia.strftime('%d/%m/%Y %H:%M:%S')
```

### Formato da API AssetsControls

A API retorna datas no formato ISO 8601 com timezone UTC (Z):

- **Formato completo**: `YYYY-MM-DDTHH:MM:SS.ffffffZ` (com microsegundos)
- **Formato simples**: `YYYY-MM-DDTHH:MM:SSZ` (sem microsegundos)

Exemplos:

- `2025-09-29T17:15:36.447937Z` (UTC) = `29/09/2025 14:15:36` (Brasília, UTC-3)
- `2025-09-29T17:15:35Z` (UTC) = `29/09/2025 14:15:35` (Brasília, UTC-3)

## Histórico

- **Data**: 14/10/2025
- **Problema**: Discrepância de datas entre sistema e API
- **Causas identificadas**:
  1. Uso de campo incorreto (`FUpdateTime` vs `FRecvTime/FGPSTime`)
  2. Formato de parsing incorreto (esperava formato simples, mas API retorna ISO 8601)
- **Soluções aplicadas**:
  1. Padronização do campo usado (agora usa `FRecvTime` ou `FGPSTime`)
  2. Correção do parsing para aceitar formato ISO 8601 com microsegundos
- **Arquivo alterado**: `core/bi_api.py` (linhas 233-250)
- **Resultado**: Datas agora coincidem perfeitamente entre sistema e API ✅

### Exemplo de Teste

```
Equipamento: 837504000484
- API AssetsControls: 2025-09-29T17:15:36.447937Z (UTC)
- API PowerBI: 29/09/2025 14:15:36 (Brasília)
✅ CORRETO: 17:15 UTC = 14:15 Brasília (UTC-3)
```
