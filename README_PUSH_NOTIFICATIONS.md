# Push Notifications - Configuração OneSignal

## 📱 Como configurar alertas no celular mesmo bloqueado

### 1. Criar conta no OneSignal

1. Acesse [onesignal.com](https://onesignal.com)
2. Crie uma conta gratuita
3. Crie um novo app

### 2. Configurar o App

1. **App ID**: Copie o App ID fornecido
2. **REST API Key**: Copie o REST API Key

### 3. Atualizar configurações

Edite o arquivo `core/settings.py`:

```python
# OneSignal Push Notifications
ONESIGNAL_APP_ID = "SEU_APP_ID_AQUI"  # Substitua pelo seu App ID
ONESIGNAL_REST_API_KEY = "SEU_REST_API_KEY_AQUI"  # Substitua pelo seu REST API Key
```

### 4. Atualizar template

No arquivo `core/templates/core/mapa.html`, substitua:

```javascript
appId: "SEU_ONESIGNAL_APP_ID_AQUI"
```

Pelo seu App ID real.

### 5. Como funciona

✅ **Alertas automáticos**: O sistema verifica a cada 30 segundos se há:
- Porta aberta (FDoor = 1)
- Luminosidade alta (fLx > 1000)

✅ **Push notifications**: Envia alertas para todos os usuários registrados

✅ **Funciona com tela bloqueada**: As notificações aparecem mesmo com o celular bloqueado

### 6. Testar

1. Acesse o mapa no navegador
2. Permita notificações quando solicitado
3. Aguarde os alertas automáticos

### 7. Personalizar

Você pode modificar:
- **Intervalo de verificação**: Altere `30000` (30 segundos) no JavaScript
- **Limite de luminosidade**: Altere `1000` no Python
- **Mensagens**: Edite os textos das notificações

### 8. Suporte

- **Android**: Funciona nativamente
- **iOS**: Requer certificado Apple Push Notification
- **Web**: Funciona em navegadores modernos

## 🚀 Resultado

Agora você receberá alertas no celular mesmo quando:
- A tela estiver bloqueada
- O navegador estiver fechado
- O celular estiver em modo silencioso

Os alertas incluem:
- 🚨 **Porta Aberta**: Quando detecta porta aberta
- 💡 **Luminosidade Alta**: Quando detecta luz forte 