class AlertsSystem {
    constructor() {
        this.alerts = [];
        this.container = null;
        this.modal = null;
        this.init();
    }

    init() {
        // Criar container de alertas
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

        // Criar modal para tratamento de eventos
        this.createModal();

        // Iniciar verificação
        this.startChecking();
    }

    createModal() {
        // Criar modal HTML
        const modalHTML = `
            <div class="modal fade" id="eventoModal" tabindex="-1" aria-labelledby="eventoModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-xl">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title" id="eventoModalLabel">
                                <i class="fas fa-exclamation-triangle"></i> Tratar Evento
                            </h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">
                                                <i class="fas fa-map-marked-alt"></i> Localização do Equipamento
                                            </h6>
                                        </div>
                                        <div class="card-body p-0">
                                            <div id="mapaEquipamento" style="height: 400px; width: 100%;"></div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="card">
                                        <div class="card-header">
                                            <h6 class="mb-0">
                                                <i class="fas fa-info-circle"></i> Informações do Evento
                                            </h6>
                                        </div>
                                        <div class="card-body">
                                            <div class="mb-3">
                                                <label class="form-label"><strong>ID do Equipamento:</strong></label>
                                                <input type="text" class="form-control" id="equipamentoId" readonly>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label"><strong>Nome:</strong></label>
                                                <input type="text" class="form-control" id="equipamentoNome" readonly>
                                            </div>
                                            <div class="mb-3">
                                                <label class="form-label"><strong>Tipo de Evento:</strong></label>
                                                <input type="text" class="form-control" id="tipoEvento" readonly>
                                            </div>
                                            <div class="mb-3" id="valorContainer" style="display: none;">
                                                <label class="form-label"><strong>Valor:</strong></label>
                                                <input type="text" class="form-control" id="valorEvento" readonly>
                                            </div>
                                            <div class="mb-3">
                                                <label for="observacao" class="form-label"><strong>Observação:</strong></label>
                                                <textarea class="form-control" id="observacao" rows="4" placeholder="Descreva a ação tomada..."></textarea>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                <i class="fas fa-times"></i> Cancelar
                            </button>
                            <button type="button" class="btn btn-success" id="btnTratarEvento">
                                <i class="fas fa-check"></i> Marcar como Tratado
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Adicionar modal ao body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Referência ao modal
        this.modal = new bootstrap.Modal(document.getElementById('eventoModal'));
        
        // Event listener para o botão de tratar
        document.getElementById('btnTratarEvento').addEventListener('click', () => {
            this.confirmarTratamento();
        });
    }

    // Função para salvar evento no backend
    salvarEventoNoBackend(evento) {
        // Montar o payload conforme esperado pelo backend
        const payload = {
            tipo_evento: evento.evento === 'aberta' ? 'aberta' : (evento.evento === 'fechada' ? 'fechada' : evento.evento),
            fonte: evento.fonte || 'Frontend',
            id_equipamento: evento.guid || evento.id_equipamento || '',
            nome_equipamento: evento.equipamento || evento.nome_equipamento || '',
            latitude: evento.lat || evento.latitude || null,
            longitude: evento.lng || evento.longitude || null,
            geofence: evento.geofence || null,
            valor: evento.valor || null,
            timestamp_evento: Math.floor(Date.now() / 1000)
        };
        fetch('/salvar-evento-frontend/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Evento salvo no backend:', data.evento_id);
            } else {
                console.error('Erro ao salvar evento no backend:', data.error);
            }
        })
        .catch(error => {
            console.error('Erro na requisição de salvamento:', error);
        });
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
        // Salvar evento no backend se for porta aberta ou fechada
        if (evento.evento === 'aberta' || evento.evento === 'fechada') {
            this.salvarEventoNoBackend(evento);
        }
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
                <div style="flex: 1;">
                    <div style="font-weight: bold; font-size: 14px; margin-bottom: 5px;">
                        ${icon} ${title}
                    </div>
                    <div style="font-size: 13px; margin-bottom: 5px;">
                        <strong>ID:</strong> ${alert.data.guid}
                    </div>
                    <div style="font-size: 13px; margin-bottom: 5px;">
                        <strong>Equipamento:</strong> ${alert.data.equipamento}${value}
                    </div>
                    <div style="font-size: 11px; opacity: 0.8; margin-top: 5px;">
                        ${new Date().toLocaleTimeString()}
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; gap: 5px; margin-left: 10px;">
                    <button id="tratar-${alert.id}" 
                            style="background: #4CAF50; border: none; color: white; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 11px;">
                        ✅ Tratar
                    </button>
                    <button id="fechar-${alert.id}" 
                            style="background: #f44336; border: none; color: white; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 11px;">
                        ✕ Fechar
                    </button>
                </div>
            </div>
        `;

        this.container.appendChild(element);
        alert.element = element;

        // Adicionar event listeners aos botões
        const tratarBtn = element.querySelector(`#tratar-${alert.id}`);
        const fecharBtn = element.querySelector(`#fechar-${alert.id}`);
        
        if (tratarBtn) {
            tratarBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.abrirModalTratamento(alert);
            });
        }
        
        if (fecharBtn) {
            fecharBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.removeAlert(alert.id);
            });
        }

        // Animar entrada
        setTimeout(() => {
            element.style.transform = 'translateX(0)';
        }, 100);

        // Auto-remover após 30 segundos
        setTimeout(() => {
            this.removeAlert(alert.id);
        }, 30000);
    }

    abrirModalTratamento(alert) {
        // Preencher informações do modal
        document.getElementById('equipamentoId').value = alert.data.guid;
        document.getElementById('equipamentoNome').value = alert.data.equipamento;
        
        const isPorta = alert.data.evento === 'aberta';
        const isLuz = alert.data.evento === 'luz';
        
        document.getElementById('tipoEvento').value = isPorta ? 'Porta Aberta' : 'Luminosidade Alta';
        
        // Mostrar/ocultar campo de valor
        const valorContainer = document.getElementById('valorContainer');
        const valorEvento = document.getElementById('valorEvento');
        
        if (isLuz) {
            valorContainer.style.display = 'block';
            valorEvento.value = `${alert.data.valor} lux`;
        } else {
            valorContainer.style.display = 'none';
            valorEvento.value = '';
        }
        
        // Limpar observação
        document.getElementById('observacao').value = '';
        
        // Armazenar alerta atual
        this.alertAtual = alert;
        
        // Abrir modal
        this.modal.show();
        
        // Carregar mapa após o modal abrir
        this.modal._element.addEventListener('shown.bs.modal', () => {
            this.carregarMapa(alert.data.guid);
        }, { once: true });
    }

    carregarMapa(equipamentoId) {
        console.log('🗺️ Carregando mapa para equipamento:', equipamentoId);
        const mapaContainer = document.getElementById('mapaEquipamento');
        
        if (!mapaContainer) {
            console.error('❌ Container do mapa não encontrado!');
            return;
        }
        
        // Limpar container
        mapaContainer.innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="spinner-border" role="status"><span class="visually-hidden">Carregando...</span></div></div>';
        
        // Criar iframe com mapa filtrado
        const iframe = document.createElement('iframe');
        const mapaUrl = `/mapa/?id=${encodeURIComponent(equipamentoId)}`;
        console.log('🔗 URL do mapa:', mapaUrl);
        
        iframe.src = mapaUrl;
        iframe.style.cssText = 'width: 100%; height: 100%; border: none; border-radius: 8px;';
        iframe.onload = () => {
            console.log('✅ Mapa carregado com sucesso para equipamento:', equipamentoId);
        };
        iframe.onerror = (error) => {
            console.error('❌ Erro ao carregar mapa:', error);
            mapaContainer.innerHTML = '<div class="alert alert-danger">Erro ao carregar o mapa. Tente novamente.</div>';
        };
        
        // Substituir spinner pelo iframe após um pequeno delay
        setTimeout(() => {
            console.log('🔄 Substituindo spinner pelo iframe...');
            mapaContainer.innerHTML = '';
            mapaContainer.appendChild(iframe);
        }, 500);
    }

    async confirmarTratamento() {
        if (!this.alertAtual) return;
        
        const observacao = document.getElementById('observacao').value;
        
        try {
            const response = await fetch('/tratar-evento/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    guid: this.alertAtual.data.guid,
                    evento: this.alertAtual.data.evento,
                    valor: this.alertAtual.data.valor,
                    observacao: observacao
                })
            });

            const data = await response.json();
            
            if (data.success) {
                console.log('✅ Evento tratado com sucesso:', data.message);
                
                // Fechar modal
                this.modal.hide();
                
                // Remover alerta
                this.removeAlert(this.alertAtual.id);
                
                // Mostrar confirmação
                this.showNotification('✅ Evento tratado com sucesso!', 'success');
                
                // Limpar alerta atual
                this.alertAtual = null;
            } else {
                console.error('❌ Erro ao tratar evento:', data.error);
                this.showNotification('❌ Erro ao tratar evento: ' + data.error, 'error');
            }
        } catch (error) {
            console.error('❌ Erro na requisição:', error);
            this.showNotification('❌ Erro na requisição', 'error');
        }
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            padding: 15px 25px;
            border-radius: 8px;
            z-index: 10000;
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        `;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
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
        const audio = document.getElementById('alert-sound');
        if (audio) {
            audio.play().catch(e => console.log('Erro ao tocar som:', e));
        }
    }

    async checkAlerts() {
        try {
            console.log('🔍 Verificando alertas...');
            const response = await fetch('/verificar-alertas/');
            const data = await response.json();
            
            console.log('📡 Resposta da API:', data);
            
            if (data.eventos && Array.isArray(data.eventos)) {
                console.log(`📋 Encontrados ${data.eventos.length} eventos`);
                data.eventos.forEach(evento => {
                    this.addAlert(evento);
                });
            } else if (data.evento && data.evento !== 'nenhum') {
                console.log('📋 Evento único encontrado:', data.evento);
                this.addAlert(data);
            } else {
                console.log('📭 Nenhum evento encontrado');
            }
        } catch (error) {
            console.error('❌ Erro ao verificar alertas:', error);
        }
    }

    startChecking() {
        // Verificar a cada 120 segundos (2 minutos) para reduzir carga na API
        setInterval(() => {
            this.checkAlerts();
        }, 120000);

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
    console.log('🚀 Inicializando sistema de alertas (alerts-system.js)...');
    
    // Verificar se já existe um sistema de alertas
    if (window.alertsSystem) {
        console.log('⚠️ Sistema de alertas já existe, não inicializando novamente');
        return;
    }
    
    window.alertsSystem = new AlertsSystem();
    console.log('✅ Sistema de alertas inicializado!');
});

// Funções globais
window.tratarEvento = (alertId) => {
    if (window.alertsSystem) {
        const alert = window.alertsSystem.alerts.find(a => a.id === alertId);
        if (alert) {
            window.alertsSystem.abrirModalTratamento(alert);
        }
    }
};

window.removeAlert = (alertId) => {
    if (window.alertsSystem) {
        window.alertsSystem.removeAlert(alertId);
    }
}; 