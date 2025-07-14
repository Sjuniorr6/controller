// Script de teste para o mapa
console.log('🗺️ Script de teste do mapa carregado');

function testarMapa() {
    console.log('🧪 Testando mapa...');
    
    // 1. Verificar se o elemento do mapa existe
    const mapElement = document.getElementById('map');
    if (mapElement) {
        console.log('✅ Elemento do mapa encontrado');
        console.log('📏 Dimensões:', mapElement.offsetWidth, 'x', mapElement.offsetHeight);
    } else {
        console.log('❌ Elemento do mapa não encontrado');
        return;
    }
    
    // 2. Verificar se o Leaflet está carregado
    if (typeof L !== 'undefined') {
        console.log('✅ Leaflet carregado');
    } else {
        console.log('❌ Leaflet não carregado');
        return;
    }
    
    // 3. Verificar se a variável map existe
    if (typeof map !== 'undefined' && map) {
        console.log('✅ Mapa inicializado');
        console.log('📍 Centro atual:', map.getCenter());
        console.log('🔍 Zoom atual:', map.getZoom());
    } else {
        console.log('❌ Mapa não inicializado');
        return;
    }
    
    // 4. Testar APIs
    testarAPIs();
}

function testarAPIs() {
    console.log('🔍 Testando APIs...');
    
    // Testar API T42
    fetch('/api/get_t42_data/')
        .then(response => {
            console.log('📡 Status T42:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('📋 Dados T42:', data);
            if (Array.isArray(data) && data.length > 0) {
                console.log('✅ API T42 funcionando -', data.length, 'equipamentos');
                
                // Testar com um ID específico
                const primeiroEquipamento = data[0];
                if (primeiroEquipamento.unitnumber) {
                    console.log('🔍 Testando busca por ID:', primeiroEquipamento.unitnumber);
                    testarBuscaPorID(primeiroEquipamento.unitnumber);
                }
            } else {
                console.log('⚠️ API T42 retornou dados vazios');
            }
        })
        .catch(error => {
            console.error('❌ Erro na API T42:', error);
        });
    
    // Testar API AssetsControls
    fetch('/api/get_assetscontrols_data/')
        .then(response => {
            console.log('📡 Status AssetsControls:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('📋 Dados AssetsControls:', data);
            if (data && data.FObject && Array.isArray(data.FObject) && data.FObject.length > 0) {
                console.log('✅ API AssetsControls funcionando -', data.FObject.length, 'equipamentos');
                
                // Testar com um ID específico
                const primeiroEquipamento = data.FObject[0];
                const id = primeiroEquipamento.FAssetID || primeiroEquipamento.FVehicleName;
                if (id) {
                    console.log('🔍 Testando busca por ID:', id);
                    testarBuscaPorID(id);
                }
            } else {
                console.log('⚠️ API AssetsControls retornou dados vazios');
            }
        })
        .catch(error => {
            console.error('❌ Erro na API AssetsControls:', error);
        });
}

function testarBuscaPorID(id) {
    console.log('🔍 Testando busca por ID:', id);
    
    // Simular busca no campo de entrada
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = id;
        console.log('✅ Campo de busca preenchido com:', id);
        
        // Chamar função de busca
        if (typeof filtrarEquipamentos === 'function') {
            console.log('🚀 Chamando filtrarEquipamentos...');
            filtrarEquipamentos();
        } else {
            console.log('❌ Função filtrarEquipamentos não encontrada');
        }
    } else {
        console.log('❌ Campo de busca não encontrado');
    }
}

function testarMarcadores() {
    console.log('📍 Testando marcadores...');
    
    if (typeof markers !== 'undefined') {
        console.log('✅ Variável markers encontrada');
        console.log('📊 Número de marcadores:', Object.keys(markers).length);
        
        Object.keys(markers).forEach((key, index) => {
            console.log(`📍 Marcador ${index + 1}:`, key);
        });
    } else {
        console.log('❌ Variável markers não encontrada');
    }
}

// Executar teste automático após 3 segundos
setTimeout(() => {
    console.log('🚀 Executando teste automático do mapa...');
    testarMapa();
    
    // Testar marcadores após 5 segundos
    setTimeout(() => {
        testarMarcadores();
    }, 2000);
}, 3000);

// Funções globais para teste manual
window.testarMapa = testarMapa;
window.testarAPIs = testarAPIs;
window.testarMarcadores = testarMarcadores; 