# Sistema de Alertas por Lotes

Este documento explica como usar o sistema de alertas organizado por lotes de equipamentos.

## 🎯 **Lotes Disponíveis**

### **Lotes de Equipamentos AssetsControls:**

| Lote | Nome | Descrição |
|------|------|-----------|
| `lote_1` | Equipamentos Principais | 10 equipamentos principais |
| `lote_2` | Equipamentos Secundários | 10 equipamentos secundários |
| `lote_3` | Equipamentos de Monitoramento | 10 equipamentos de monitoramento |
| `lote_4` | Equipamentos de Controle | 10 equipamentos de controle |
| `lote_5` | Equipamentos de Logística | 10 equipamentos de logística |
| `lote_6` | Equipamentos de Transporte | 10 equipamentos de transporte |
| `lote_7` | Equipamentos de Armazenamento | 10 equipamentos de armazenamento |
| `lote_8` | Equipamentos de Distribuição | 10 equipamentos de distribuição |
| `lote_9` | Equipamentos de Produção | 10 equipamentos de produção |
| `lote_10` | Equipamentos de Qualidade | 10 equipamentos de qualidade |

## 🔧 **Como Usar**

### **1. Monitorar Todos os Equipamentos (Padrão)**
```javascript
// Monitora todos os equipamentos (AssetsControls + T42)
verificarPorta();
```

### **2. Monitorar Lote Específico**
```javascript
// Monitora apenas equipamentos do lote_1
verificarPorta('lote_1');

// Monitora apenas equipamentos do lote_6
verificarPorta('lote_6');
```

### **3. Via API Direta**
```bash
# Monitorar todos os equipamentos
curl "http://localhost:8000/verificar-alertas/"

# Monitorar lote específico
curl "http://localhost:8000/verificar-alertas/?lote=lote_1"

# Monitorar apenas AssetsControls de um lote
curl "http://localhost:8000/verificar-fdoor/?lote=lote_6"
```

## 📡 **Endpoints Disponíveis**

### **Com Suporte a Lotes:**
- `/verificar-alertas/` - Ambos os sistemas (AssetsControls + T42)
- `/verificar-fdoor/` - Apenas AssetsControls

### **Sem Suporte a Lotes (Sempre Todos):**
- `/verificar-t42-door/` - Apenas T42 (sempre todos os equipamentos)

## 🎯 **Exemplos de Uso**

### **Monitoramento por Cliente:**
```javascript
// Para cliente "Alto Cafezal" - usar lote específico
setInterval(() => verificarPorta('lote_1'), 15000);

// Para cliente "Bourbon Coffee" - usar lote específico  
setInterval(() => verificarPorta('lote_2'), 15000);
```

### **Monitoramento por Tipo:**
```javascript
// Monitorar apenas equipamentos de transporte
setInterval(() => verificarPorta('lote_6'), 15000);

// Monitorar apenas equipamentos de produção
setInterval(() => verificarPorta('lote_9'), 15000);
```

## 📊 **Resposta da API**

### **Com Lote Específico:**
```json
{
    "evento": "aberta",
    "equipamento": "Equipamento 123",
    "guid": "f0d11885-b7db-4565-a7d1-14f3e8faa362",
    "lote": "lote_6",
    "fonte": "AssetsControls"
}
```

### **Sem Lote (Todos):**
```json
{
    "evento": "aberta", 
    "equipamento": "Equipamento 456",
    "guid": "abc123...",
    "lote": "todos",
    "fonte": "T42"
}
```

## 🎨 **Interface Visual**

### **Popup de Alerta:**
- **Com lote:** "Equipamento 123 (TETIS) - AssetsControls [lote_6]"
- **Sem lote:** "Equipamento 456 (TETIS) - T42"

## 🔧 **Configuração de Lotes**

### **Adicionar Novo Lote:**
Edite o arquivo `core/equipament_cnfig.py`:

```python
EQUIPMENT_LOTS = {
    "lote_11": {
        "nome": "Lote 11 - Novos Equipamentos",
        "guids": [
            'novo-guid-1',
            'novo-guid-2',
            'novo-guid-3'
        ]
    }
}
```

### **Modificar Lote Existente:**
```python
"lote_1": {
    "nome": "Lote 1 - Equipamentos Principais Atualizados",
    "guids": [
        'guid-atualizado-1',
        'guid-atualizado-2'
    ]
}
```

## 🚀 **Vantagens do Sistema por Lotes**

1. **Performance:** Menos equipamentos = requisições mais rápidas
2. **Organização:** Equipamentos agrupados por função/cliente
3. **Flexibilidade:** Pode monitorar apenas equipamentos relevantes
4. **Escalabilidade:** Fácil adicionar novos lotes conforme necessário

## 🧪 **Testando**

### **Teste Manual:**
```bash
# Testar lote específico
curl "http://localhost:8000/verificar-fdoor/?lote=lote_1"

# Testar todos os equipamentos
curl "http://localhost:8000/verificar-fdoor/"
```

### **Teste no Frontend:**
```javascript
// No console do navegador
verificarPorta('lote_6');  // Testar lote específico
verificarPorta();          // Testar todos
```

## 📈 **Próximos Passos**

1. **Interface de Seleção:** Criar dropdown para escolher lotes
2. **Múltiplos Lotes:** Permitir selecionar vários lotes simultaneamente
3. **Configuração Dinâmica:** Interface para gerenciar lotes
4. **Relatórios por Lote:** Estatísticas específicas por lote 