// Script de teste simples para verificar alertas
console.log('🧪 Script de teste de alertas carregado');

// Função para testar alertas
function testarAlertas() {
    console.log('🧪 Testando sistema de alertas...');
    
    if (window.alertsSystem) {
        console.log('✅ Sistema de alertas encontrado');
        
        // Testar alerta de porta
        const eventoPorta = {
            id: 'teste_porta_' + Date.now(),
            evento: 'aberta',
            equipamento: 'TESTE-001',
            guid: 'TESTE-001',
            timestamp: Date.now()
        };
        
        // Testar alerta de luminosidade
        const eventoLuz = {
            id: 'teste_luz_' + Date.now(),
            evento: 'luz',
            equipamento: 'TESTE-002',
            guid: 'TESTE-002',
            valor: 150.5,
            timestamp: Date.now()
        };
        
        console.log('📋 Adicionando alertas de teste...');
        window.alertsSystem.addAlert(eventoPorta);
        
        setTimeout(() => {
            window.alertsSystem.addAlert(eventoLuz);
        }, 2000);
        
    } else {
        console.log('❌ Sistema de alertas não encontrado');
    }
}

// Função para testar a API diretamente
function testarAPI() {
    console.log('🔍 Testando API de alertas...');
    
    fetch('/verificar-fdoor/')
        .then(response => {
            console.log('📡 Status da resposta:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('📋 Dados da API:', data);
            
            if (data.eventos && data.eventos.length > 0) {
                console.log(`🎯 Encontrados ${data.eventos.length} eventos na API`);
                
                // Se o sistema de alertas estiver disponível, adicionar os alertas
                if (window.alertsSystem) {
                    console.log('📋 Adicionando eventos da API ao sistema de alertas...');
                    data.eventos.forEach((evento, index) => {
                        console.log(`📋 Adicionando evento ${index + 1}:`, evento);
                        window.alertsSystem.addAlert(evento);
                    });
                } else {
                    console.log('❌ Sistema de alertas não disponível para adicionar eventos');
                }
            } else {
                console.log('📭 Nenhum evento encontrado na API');
            }
        })
        .catch(error => {
            console.error('❌ Erro ao testar API:', error);
        });
}

// Executar teste automático após 2 segundos
setTimeout(() => {
    console.log('🚀 Iniciando testes automáticos...');
    testarAPI();
    
    // Testar alertas de exemplo após 3 segundos
    setTimeout(() => {
        testarAlertas();
    }, 3000);
}, 2000);

// Adicionar botão de teste na página
document.addEventListener('DOMContentLoaded', () => {
    const testButton = document.createElement('button');
    testButton.textContent = '🧪 Testar Alertas';
    testButton.style.cssText = `
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 10000;
        background: #2196F3;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-family: Arial, sans-serif;
    `;
    
    testButton.addEventListener('click', testarAlertas);
    document.body.appendChild(testButton);
    
    console.log('🧪 Botão de teste adicionado');
});

// Função global para teste
window.testarAlertas = testarAlertas; 