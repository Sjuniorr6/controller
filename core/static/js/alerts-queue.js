class AlertsQueue {
    constructor() {
        this.alerts = [];
        this.isPlaying = false;
        this.container = null;
        this.init();
    }

    init() {
        // Criar container de alertas se não existir
        if (!document.getElementById('alerts-container')) {
            this.container = document.createElement('div');
            this.container.id = 'alerts-container';
            this.container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(this.container);
        } else {
            this.container = document.getElementById('alerts-container');
        }

        // Iniciar verificação de alertas
        this.startChecking();
    }

    addAlert(evento) {
        const alertId = evento.id || `alerta_${Date.now()}_${Math.random()}`;
        
        // Verificar se já existe este alerta
        if (this.alerts.find(a => a.id === alertId)) {
            return;
        }

        const alert = {
            id: alertId,
            data: evento,
            element: null,
            timestamp: Date.now()
        };

        this.alerts.push(alert);
        this.createAlertElement(alert);
        this.playSound();
    }

    createAlertElement(alert) {
        const element = document.createElement('div');
        element.className = 'alert-card';
        element.id = `alert-${alert.id}`;
        
        const isPorta = alert.data.evento === 'aberta';
        const isLuz = alert.data.evento === 'luz';
        
        element.style.cssText = `
            background: ${isPorta ? '#ff4444' : '#ff8800'};
            color: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transform: translateX(100%);
            transition: transform 0.5s ease-out;
            pointer-events: auto;
            cursor: pointer;
            max-width: 350px;
            font-family: Arial, sans-serif;
        `;

        const icon = isPorta ? '🚪' : '💡';
        const title = isPorta ? 'PORTA ABERTA' : 'LUMINOSIDADE ALTA';
        const value = isLuz ? ` (${alert.data.valor} lux)` : '';
        
        element.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px;">
                        ${icon} ${title}
                    </div>
                    <div style="font-size: 13px;">
                        ${alert.data.equipamento}${value}
                    </div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 5px;">
                        ${new Date().toLocaleTimeString()}
                    </div>
                </div>
                <button onclick="alertsQueue.removeAlert('${alert.id}')" 
                        style="background: none; border: none; color: white; font-size: 18px; cursor: pointer; padding: 0; margin-left: 10px;">
                    ✕
                </button>
            </div>
        `;

        this.container.appendChild(element);
        alert.element = element;

        // Animar entrada
        setTimeout(() => {
            element.style.transform = 'translateX(0)';
        }, 100);

        // Auto-remover após 10 segundos
        setTimeout(() => {
            this.removeAlert(alert.id);
        }, 10000);
    }

    removeAlert(alertId) {
        const alert = this.alerts.find(a => a.id === alertId);
        if (!alert || !alert.element) return;

        // Animar saída
        alert.element.style.transform = 'translateX(100%)';
        
        setTimeout(() => {
            if (alert.element && alert.element.parentNode) {
                alert.element.parentNode.removeChild(alert.element);
            }
            this.alerts = this.alerts.filter(a => a.id !== alertId);
        }, 500);
    }

    playSound() {
        // Tocar som de alerta se disponível
        const audio = document.getElementById('alert-sound');
        if (audio) {
            audio.play().catch(e => console.log('Erro ao tocar som:', e));
        }
    }

    async checkAlerts() {
        try {
            console.log('🔍 Verificando alertas...');
            const response = await fetch('/verificar-fdoor/');
            const data = await response.json();
            
            console.log('📡 Resposta da API:', data);
            
            // Formato novo: lista de eventos
            if (data.eventos && Array.isArray(data.eventos)) {
                console.log(`📋 Encontrados ${data.eventos.length} eventos`);
                data.eventos.forEach(evento => {
                    this.addAlert(evento);
                });
            }
            // Formato antigo: evento único
            else if (data.evento && data.evento !== 'nenhum') {
                console.log('📋 Evento único encontrado:', data.evento);
                this.addAlert(data);
            }
            else {
                console.log('📭 Nenhum evento encontrado');
            }
        } catch (error) {
            console.error('❌ Erro ao verificar alertas:', error);
        }
    }

    startChecking() {
        // Verificar a cada 5 segundos
        setInterval(() => {
            this.checkAlerts();
        }, 5000);

        // Primeira verificação imediata
        this.checkAlerts();
    }

    clearAll() {
        this.alerts.forEach(alert => {
            this.removeAlert(alert.id);
        });
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Inicializando sistema de alertas...');
    window.alertsQueue = new AlertsQueue();
    console.log('✅ Sistema de alertas inicializado!');
});

// Função global para remover alertas
window.removeAlert = (alertId) => {
    if (window.alertsQueue) {
        window.alertsQueue.removeAlert(alertId);
    }
}; 