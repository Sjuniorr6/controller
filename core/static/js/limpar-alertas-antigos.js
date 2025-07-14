// Script para limpar alertas antigos
console.log('🧹 Script de limpeza de alertas carregado');

function limparAlertasAntigos() {
    console.log('🧹 Limpando alertas antigos...');
    
    // Remover alertas criados pelo sistema antigo (alerts-queue.js)
    const alertasAntigos = document.querySelectorAll('.alert-card');
    console.log(`🧹 Encontrados ${alertasAntigos.length} alertas antigos`);
    
    alertasAntigos.forEach((alerta, index) => {
        console.log(`🧹 Removendo alerta ${index + 1}`);
        if (alerta.parentNode) {
            alerta.parentNode.removeChild(alerta);
        }
    });
    
    // Remover popups antigos (custom-popup)
    const popupsAntigos = document.querySelectorAll('.custom-popup, .popup-overlay');
    console.log(`🧹 Encontrados ${popupsAntigos.length} popups antigos`);
    
    popupsAntigos.forEach((popup, index) => {
        console.log(`🧹 Removendo popup ${index + 1}`);
        if (popup.parentNode) {
            popup.parentNode.removeChild(popup);
        }
    });
    
    // Remover alertas simples criados pelo test-alerts.js
    const alertasSimples = document.querySelectorAll('div[style*="position: fixed"][style*="right: 20px"]');
    console.log(`🧹 Encontrados ${alertasSimples.length} alertas simples`);
    
    alertasSimples.forEach((alerta, index) => {
        console.log(`🧹 Removendo alerta simples ${index + 1}`);
        if (alerta.parentNode) {
            alerta.parentNode.removeChild(alerta);
        }
    });
    
    console.log('✅ Limpeza concluída!');
}

// Executar limpeza quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    // Aguardar um pouco para garantir que todos os scripts carregaram
    setTimeout(limparAlertasAntigos, 1000);
});

// Função global para limpeza manual
window.limparAlertasAntigos = limparAlertasAntigos;

// Executar limpeza a cada 30 segundos para garantir
setInterval(limparAlertasAntigos, 30000); 