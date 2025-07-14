// Script de diagnóstico para problemas com o mapa no modal
class DiagnosticoMapa {
    constructor() {
        this.resultados = [];
    }

    async executarDiagnostico() {
        console.log('🔍 Iniciando diagnóstico do mapa...');
        this.resultados = [];

        // 1. Verificar se o sistema de alertas está carregado
        this.verificarSistemaAlertas();

        // 2. Verificar se o modal existe
        this.verificarModal();

        // 3. Verificar se a URL do mapa funciona
        await this.verificarUrlMapa();

        // 4. Verificar se o iframe pode ser criado
        this.verificarIframe();

        // 5. Mostrar resultados
        this.mostrarResultados();
    }

    verificarSistemaAlertas() {
        console.log('🔍 Verificando sistema de alertas...');
        
        if (window.alertsSystem) {
            this.adicionarResultado('✅ Sistema de alertas carregado', 'success');
            
            if (window.alertsSystem.modal) {
                this.adicionarResultado('✅ Modal do sistema de alertas encontrado', 'success');
            } else {
                this.adicionarResultado('❌ Modal do sistema de alertas não encontrado', 'error');
            }
        } else {
            this.adicionarResultado('❌ Sistema de alertas não carregado', 'error');
        }
    }

    verificarModal() {
        console.log('🔍 Verificando modal...');
        
        const modal = document.getElementById('eventoModal');
        if (modal) {
            this.adicionarResultado('✅ Modal encontrado no DOM', 'success');
            
            const mapaContainer = document.getElementById('mapaEquipamento');
            if (mapaContainer) {
                this.adicionarResultado('✅ Container do mapa encontrado', 'success');
            } else {
                this.adicionarResultado('❌ Container do mapa não encontrado', 'error');
            }
        } else {
            this.adicionarResultado('❌ Modal não encontrado no DOM', 'error');
        }
    }

    async verificarUrlMapa() {
        console.log('🔍 Verificando URL do mapa...');
        
        try {
            const response = await fetch('/mapa/?id=TESTE-001');
            if (response.ok) {
                this.adicionarResultado('✅ URL do mapa responde corretamente', 'success');
            } else {
                this.adicionarResultado(`❌ URL do mapa retornou status ${response.status}`, 'error');
            }
        } catch (error) {
            this.adicionarResultado(`❌ Erro ao acessar URL do mapa: ${error.message}`, 'error');
        }
    }

    verificarIframe() {
        console.log('🔍 Verificando criação de iframe...');
        
        try {
            const iframe = document.createElement('iframe');
            iframe.src = '/mapa/?id=TESTE-001';
            iframe.style.cssText = 'width: 100%; height: 100%; border: none;';
            
            this.adicionarResultado('✅ Iframe criado com sucesso', 'success');
        } catch (error) {
            this.adicionarResultado(`❌ Erro ao criar iframe: ${error.message}`, 'error');
        }
    }

    adicionarResultado(mensagem, tipo) {
        this.resultados.push({ mensagem, tipo, timestamp: new Date().toLocaleTimeString() });
        console.log(`${tipo === 'success' ? '✅' : '❌'} ${mensagem}`);
    }

    mostrarResultados() {
        console.log('📊 Resultados do diagnóstico:');
        this.resultados.forEach((resultado, index) => {
            console.log(`${index + 1}. [${resultado.timestamp}] ${resultado.mensagem}`);
        });
    }
}

// Função global para executar diagnóstico
window.executarDiagnosticoMapa = () => {
    const diagnostico = new DiagnosticoMapa();
    diagnostico.executarDiagnostico();
};

// Função para diagnosticar especificamente os alertas
window.diagnosticarAlertas = async () => {
    console.log('🔍 Iniciando diagnóstico dos alertas...');
    
    // 1. Verificar se a API está funcionando
    console.log('🔍 Testando API de alertas...');
    try {
        const response = await fetch('/verificar-fdoor/');
        const data = await response.json();
        
        console.log('📡 Resposta da API:', data);
        
        if (data.eventos && data.eventos.length > 0) {
            console.log(`✅ API funcionando - ${data.eventos.length} eventos encontrados`);
            
            // 2. Verificar se o sistema de alertas está disponível
            if (window.alertsSystem) {
                console.log('✅ Sistema de alertas disponível');
                
                // 3. Tentar adicionar um evento
                console.log('🔍 Tentando adicionar evento ao sistema...');
                const primeiroEvento = data.eventos[0];
                window.alertsSystem.addAlert(primeiroEvento);
                console.log('✅ Evento adicionado ao sistema');
                
                // 4. Verificar se o alerta foi criado
                setTimeout(() => {
                    const alertas = document.querySelectorAll('.alert-card');
                    console.log(`📊 Alertas visíveis na página: ${alertas.length}`);
                    
                    if (alertas.length > 0) {
                        console.log('✅ Alertas estão sendo exibidos corretamente');
                    } else {
                        console.log('❌ Alertas não estão sendo exibidos');
                        
                        // Verificar se o container existe
                        const container = document.getElementById('alerts-container');
                        if (container) {
                            console.log('✅ Container de alertas existe');
                            console.log('📋 Conteúdo do container:', container.innerHTML);
                        } else {
                            console.log('❌ Container de alertas não existe');
                        }
                    }
                }, 1000);
                
            } else {
                console.log('❌ Sistema de alertas não disponível');
            }
        } else {
            console.log('📭 Nenhum evento encontrado na API');
        }
    } catch (error) {
        console.error('❌ Erro ao testar API:', error);
    }
};

// Executar diagnóstico automático após 3 segundos
setTimeout(() => {
    console.log('🚀 Executando diagnóstico automático dos alertas...');
    window.diagnosticarAlertas();
}, 3000); 