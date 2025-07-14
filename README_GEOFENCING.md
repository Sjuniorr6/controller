# Sistema de Geofencing - Cercas Virtuais

## 🚫 Como funciona

O sistema implementa **cercas virtuais (geofencing)** de **5km** ao redor das fazendas da Nestlé para **bloquear alertas** quando os equipamentos estiverem dentro dessas áreas.

## 📍 Fazendas com Cercas Virtuais

### 1. **ALTO CAFEZAL**
- **Endereço**: Rua Coronel João Cândico de Aguiar, 2101 - Patrocínio/MG
- **Coordenadas**: -18.9444, -47.0000
- **Raio**: 5km

### 2. **BOURBON SPECIALTY COFFEES**
- **Endereço**: Rua Piauí, 129 - Poços de Caldas/MG
- **Coordenadas**: -21.7878, -46.5614
- **Raio**: 5km

### 3. **CARMO COFFEE**
- **Endereço**: Rod. Fernão Dias, S/N - Três Corações/MG
- **Coordenadas**: -21.6969, -45.2533
- **Raio**: 5km

### 4. **COOXUPÉ**
- **Endereço**: Rua Manoel Gonçalves Ferraz, 356 - Guaxupé/MG
- **Coordenadas**: -21.3056, -46.7089
- **Raio**: 5km

### 5. **EXPOCACCER**
- **Endereço**: Avenida Faria Pereira, 3945 - Patrocínio/MG
- **Coordenadas**: -18.9444, -47.0000
- **Raio**: 5km

### 6. **NKG**
- **Endereço**: Av. José Ribeiro Tristão, 105 - Varginha/MG
- **Coordenadas**: -21.5514, -45.4303
- **Raio**: 5km

### 7. **VELOSO COFFEE**
- **Endereço**: Avenida Bela Vista, 81 - Carmo do Paranaíba/MG
- **Coordenadas**: -19.0000, -46.3167
- **Raio**: 5km

### 8. **VELOSO GREEN COFFEE**
- **Endereço**: Avenida João Batista da Silva, 801 - Carmo do Paranaíba/MG
- **Coordenadas**: -19.0000, -46.3167
- **Raio**: 5km

### 9. **VOLCAFÉ**
- **Endereço**: Rua Maria Nazareth Prado, 225 - Varginha/MG
- **Coordenadas**: -21.5514, -45.4303
- **Raio**: 5km

## 🔧 Como funciona tecnicamente

### 1. **Cálculo de Distância**
- Usa a **fórmula de Haversine** para calcular a distância entre dois pontos geográficos
- Considera a curvatura da Terra para precisão

### 2. **Verificação de Geofencing**
- Para cada equipamento, verifica se está dentro de alguma cerca
- Se estiver dentro de uma cerca: **alerta bloqueado**
- Se estiver fora de todas as cercas: **alerta permitido**

### 3. **Logs do Sistema**
```
🚫 Alerta bloqueado: [Nome do Equipamento] está dentro da cerca de [Nome da Fazenda]
```

## ✅ Benefícios

1. **Reduz falsos positivos** - Não alerta quando equipamento está na fazenda
2. **Foco em eventos reais** - Só alerta quando há situação suspeita
3. **Configurável** - Fácil adicionar/remover fazendas
4. **Preciso** - Usa coordenadas GPS reais

## 🔄 Como adicionar novas fazendas

Edite o arquivo `core/views.py` e adicione na variável `FAZENDAS_GEOFENCING`:

```python
'NOVA_FAZENDA': {
    'nome': 'NOME COMPLETO DA FAZENDA',
    'lat': -XX.XXXX,  # Latitude
    'lng': -XX.XXXX,  # Longitude
    'raio_km': 5
}
```

## 📊 Monitoramento

O sistema mostra no console quando um alerta é bloqueado:
- **Equipamento**: Nome do equipamento
- **Fazenda**: Qual fazenda está bloqueando
- **Distância**: Distância calculada até o centro da fazenda

## 🎯 Resultado

- **Dentro das fazendas**: ❌ Alertas bloqueados
- **Fora das fazendas**: ✅ Alertas funcionam normalmente
- **Porta aberta**: Só alerta se estiver fora das cercas
- **Luminosidade alta**: Só alerta se estiver fora das cercas 