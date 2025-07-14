// Script de teste simples para alertas
console.log('🧪 Script de teste carregado');

function testAlerts() {
    console.log('🧪 Testando alertas...');
    
    fetch('/verificar-fdoor/')
        .then(response => response.json())
        .then(data => {
            console.log('📡 Dados recebidos:', data);
            
            if (data.eventos && data.eventos.length > 0) {
                console.log(`🎯 Encontrados ${data.eventos.length} eventos!`);
                
                // Mostrar apenas os primeiros 3 eventos para teste
                data.eventos.slice(0, 3).forEach((evento, index) => {
                    console.log(`📋 Evento ${index + 1}:`, evento);
                    
                    // Criar alerta simples
                    const alertDiv = document.createElement('div');
                    alertDiv.style.cssText = `
                        position: fixed;
                        top: ${20 + (index * 80)}px;
                        right: 20px;
                        background: ${evento.evento === 'aberta' ? '#ff4444' : '#ff8800'};
                        color: white;
                        padding: 15px;
                        border-radius: 8px;
                        z-index: 9999;
                        max-width: 300px;
                        font-family: Arial, sans-serif;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                    `;
                    
                    alertDiv.innerHTML = `
                        <div style="font-weight: bold; margin-bottom: 5px;">
                            ${evento.evento === 'aberta' ? '🚪 PORTA ABERTA' : '💡 LUMINOSIDADE ALTA'}
                        </div>
                        <div>${evento.equipamento}</div>
                        ${evento.valor ? `<div>${evento.valor} lux</div>` : ''}
                    `;
                    
                    document.body.appendChild(alertDiv);
                    
                    // Remover após 5 segundos
                    setTimeout(() => {
                        if (alertDiv.parentNode) {
                            alertDiv.parentNode.removeChild(alertDiv);
                        }
                    }, 5000);
                });
            } else {
                console.log('📭 Nenhum evento encontrado');
            }

            if (data.length === 1) {
                map.setView([data[0].lat, data[0].lng], 16);
                // Adicione marcador, etc.
            }
        })
        .catch(error => {
            console.error('❌ Erro:', error);
        });
}

// NÃO testar automaticamente - apenas quando chamado manualmente
// testAlerts();

// NÃO testar a cada 10 segundos - comentado para evitar conflitos
// setInterval(testAlerts, 10000);

console.log('🧪 Teste configurado - use testAlerts() no console para testar manualmente');

// Função global para teste manual
window.testAlerts = testAlerts; 