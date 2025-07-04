// Script para testar o modal de tratamento
console.log('🧪 Script de teste do modal carregado');

function testarModal() {
    console.log('🧪 Testando modal de tratamento...');
    
    if (window.alertsSystem) {
        console.log('✅ Sistema de alertas encontrado');
        
        // Simular um evento de porta aberta
        const eventoTeste = {
            id: 'teste_modal_' + Date.now(),
            evento: 'aberta',
            equipamento: 'TESTE-MODAL-001',
            guid: 'TESTE-MODAL-001',
            timestamp: Date.now()
        };
        
        console.log('📋 Abrindo modal para evento:', eventoTeste);
        window.alertsSystem.abrirModalTratamento({
            id: eventoTeste.id,
            data: eventoTeste
        });
        
    } else {
        console.log('❌ Sistema de alertas não encontrado');
    }
}

function testarMapaDireto() {
    console.log('🧪 Testando carregamento direto do mapa...');
    
    // Testar se a URL do mapa funciona
    const testUrl = '/mapa/?id=TESTE-MAP-001';
    console.log('🔗 Testando URL:', testUrl);
    
    fetch(testUrl)
        .then(response => {
            console.log('📡 Resposta do mapa:', response.status, response.statusText);
            if (response.ok) {
                console.log('✅ URL do mapa está funcionando');
            } else {
                console.log('❌ URL do mapa retornou erro:', response.status);
            }
        })
        .catch(error => {
            console.error('❌ Erro ao testar URL do mapa:', error);
        });
}

function testarModalComMapa() {
    console.log('🧪 Testando modal com mapa...');
    
    // Criar um modal de teste simples
    const modalHTML = `
        <div class="modal fade" id="testeModal" tabindex="-1">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Teste de Mapa</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div id="testeMapaContainer" style="height: 400px; width: 100%; border: 1px solid #ccc;">
                            <div class="d-flex justify-content-center align-items-center h-100">
                                <div class="spinner-border" role="status">
                                    <span class="visually-hidden">Carregando...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Adicionar modal ao body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Criar iframe de teste
    const container = document.getElementById('testeMapaContainer');
    const iframe = document.createElement('iframe');
    iframe.src = '/mapa/?id=TESTE-MAP-001';
    iframe.style.cssText = 'width: 100%; height: 100%; border: none;';
    iframe.onload = () => console.log('✅ Iframe de teste carregado');
    iframe.onerror = (e) => console.error('❌ Erro no iframe de teste:', e);
    
    // Substituir spinner pelo iframe
    setTimeout(() => {
        container.innerHTML = '';
        container.appendChild(iframe);
    }, 1000);
    
    // Abrir modal
    const modal = new bootstrap.Modal(document.getElementById('testeModal'));
    modal.show();
}

// Adicionar botão de teste na página
document.addEventListener('DOMContentLoaded', () => {
    const testButton = document.createElement('button');
    testButton.textContent = '🧪 Testar Modal';
    testButton.style.cssText = `
        position: fixed;
        top: 50px;
        left: 10px;
        z-index: 10000;
        background: #9C27B0;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-family: Arial, sans-serif;
    `;
    
    testButton.addEventListener('click', testarModal);
    document.body.appendChild(testButton);
    
    console.log('🧪 Botão de teste do modal adicionado');
});

// Adicionar funções ao window para teste via console
window.testarModal = testarModal;
window.testarMapaDireto = testarMapaDireto;
window.testarModalComMapa = testarModalComMapa; 