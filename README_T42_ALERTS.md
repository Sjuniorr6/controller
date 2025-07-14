# Sistema de Alertas T42

Este documento explica como funciona o novo sistema de alertas para dispositivos T42 (Golden/Tetis) implementado no projeto.

## 🚀 Funcionalidades

O sistema agora monitora **ambos os tipos de dispositivos**:
- **AssetsControls** (sistema existente)
- **T42/Golden/Tetis** (novo sistema)

### Alertas Monitorados

1. **🚪 Porta Aberta/Fechada**
   - Detecta mudanças de status da porta
   - Suporta modelos: Tetis, Watchlock, Kylos

2. **💡 Luminosidade Alta**
   - Alerta quando luminosidade > 15 lux
   - Disponível para todos os dispositivos T42

## 🔧 Implementação

### Novas Funções

#### 1. `verificar_t42_door(request)`
```python
# Endpoint: /verificar-t42-door/
# Monitora dispositivos T42 especificamente
```

#### 2. `verificar_alertas_geral(request)`
```python
# Endpoint: /verificar-alertas/
# Combina verificação de AssetsControls + T42
```

### Endpoints Disponíveis

| Endpoint | Função | Descrição |
|----------|--------|-----------|
| `/verificar-fdoor/` | `verificar_fdoor` | Apenas AssetsControls |
| `/verificar-t42-door/` | `verificar_t42_door` | Apenas T42 |
| `/verificar-alertas/` | `verificar_alertas_geral` | Ambos os sistemas |

## 📡 API T42

### Configurações
```python
T42_API_URL = "https://mongol.brono.com/mongol/api.php"
T42_USER = "wimc_u_nestle"
T42_PASS = "Inte@20xx"
```

### Comandos Utilizados

1. **`get_units`** - Lista todos os equipamentos
2. **`get_last_transmit`** - Última transmissão de um equipamento

### Campos Monitorados

#### Porta
- **Campo:** `door`
- **Valores:** 
  - `"0"` = Porta Aberta
  - `"1"` = Porta Fechada
- **Modelos suportados:** Tetis, Watchlock, Kylos

#### Luminosidade
- **Campo:** `light`
- **Valor:** Número inteiro (lux)
- **Alerta:** > 15 lux

## 🔄 Como Funciona

### 1. Verificação Periódica
```javascript
// A cada 15 segundos (base.html)
setInterval(verificarPorta, 15000);
```

### 2. Cache de Status
```python
# Armazena status anterior para detectar mudanças
ultimo_status_porta = cache.get(f't42_ultimo_status_porta_{unit_number}')
cache.set(f't42_ultimo_status_porta_{unit_number}', door_status, timeout=3600)
```

### 3. Detecção de Mudanças
```python
# Porta abre
if door_status == 0 and ultimo_status_porta != 0:
    return JsonResponse({'evento': 'aberta', 'equipamento': nome})

# Porta fecha  
elif door_status == 1 and ultimo_status_porta == 0:
    return JsonResponse({'evento': 'fechada', 'equipamento': nome})
```

## 🧪 Testando

### Script de Teste
Execute o script `test_t42_alerts.py` para verificar:

```bash
python test_t42_alerts.py
```

### Teste Manual
```bash
# Testar endpoint T42
curl http://localhost:8000/verificar-t42-door/

# Testar endpoint combinado
curl http://localhost:8000/verificar-alertas/
```

## 📊 Resposta da API

### Sucesso
```json
{
    "evento": "aberta",
    "equipamento": "Nome do Equipamento",
    "valor": 25,
    "unit_number": "123456",
    "modelo": "Tetis"
}
```

### Sem Eventos
```json
{
    "evento": "nenhum",
    "equipamento": ""
}
```

## 🎯 Alertas Visuais

### Popup de Alerta
- **Porta Aberta:** 🚨 Fundo vermelho
- **Porta Fechada:** ✅ Fundo verde  
- **Luminosidade:** 💡 Fundo laranja

### Som de Alerta
- Arquivo: `/static/som-alerta.mp3`
- Toca automaticamente em qualquer evento

## 🔧 Configurações

### Limite de Luminosidade
```python
# Em verificar_t42_door()
if light_value > 15:  # Alerta se > 15 lux
```

### Intervalo de Verificação
```javascript
// Em base.html
setInterval(verificarPorta, 15000); // 15 segundos
```

### Timeout do Cache
```python
# Cache expira em 1 hora
cache.set(key, value, timeout=3600)
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de API T42**
   - Verificar credenciais
   - Verificar conectividade com `https://mongol.brono.com`

2. **Dispositivos não aparecem**
   - Verificar se o modelo é suportado (Tetis, Watchlock, Kylos)
   - Verificar se o campo `door` está disponível

3. **Alertas não funcionam**
   - Verificar se o cache está funcionando
   - Verificar logs do Django

### Logs Úteis
```python
print(f"Erro ao verificar dispositivos T42: {e}")
print(f"Equipamento: {unit_name} - Status porta: {door_status}")
```

## 📈 Próximos Passos

1. **Filtros por Lote** - Implementar filtros específicos por cliente
2. **Histórico de Alertas** - Salvar alertas no banco de dados
3. **Notificações Push** - Integrar com sistema de notificações
4. **Dashboard de Alertas** - Interface para gerenciar alertas

## 🔐 Segurança

- Credenciais da API T42 devem ser protegidas
- Considerar usar variáveis de ambiente
- Implementar rate limiting se necessário 