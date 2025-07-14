// Função para abrir o modal de edição
function abrirModalEdicaoFrontend(row) {
    // Preenche o modal com os valores atuais das células da tabela
    document.getElementById('modalUnitId').value = row.cells[0].textContent.trim();
    document.getElementById('modalBL').value = row.cells[4].textContent.trim();
    document.getElementById('modalContainer').value = row.cells[5].textContent.trim();
    document.getElementById('modalDestino').value = row.cells[6].textContent.trim();
    document.getElementById('modalBateria').value = row.cells[1].textContent.trim();
    document.getElementById('modalPorta').value = row.cells[2].textContent.trim();
    document.getElementById('modalLuminosidade').value = row.cells[3].textContent.trim();
    document.getElementById('modalLocalizacao').value = row.cells[7].textContent.trim();
    document.getElementById('modalAtualizacao').value = row.cells[8].textContent.trim();
    
    // Salva referência da linha para edição
    document.getElementById('editEquipForm').dataset.currentRow = row.rowIndex;
    
    // Abre o modal
    var myModal = new bootstrap.Modal(document.getElementById('editEquipModal'));
    myModal.show();
}

// Configurar o botão de salvar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    const salvarBtn = document.getElementById('salvarEdicaoBtn');
    if (salvarBtn) {
        salvarBtn.onclick = function() {
            const form = document.getElementById('editEquipForm');
            const rowIndex = parseInt(form.dataset.currentRow);
            
            if (rowIndex) {
                const tabela = document.getElementById("resultadosTabelaBody");
                const row = tabela.rows[rowIndex - 1]; // rowIndex é 1-based
                
                if (row) {
                    // Dados para enviar ao backend
                    const dados = {
                        unitnumber: document.getElementById('modalUnitId').value,
                        BL: document.getElementById('modalBL').value,
                        container: document.getElementById('modalContainer').value,
                        destino: document.getElementById('modalDestino').value
                    };
                    
                    // Faz a chamada AJAX para salvar no banco
                    fetch('/equipamentos/api/atualizar-campos-modal/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(dados)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Atualiza os campos editáveis na linha da tabela
                            row.cells[4].textContent = document.getElementById('modalBL').value;
                            row.cells[5].textContent = document.getElementById('modalContainer').value;
                            row.cells[6].textContent = document.getElementById('modalDestino').value;
                            
                            console.log('Campos atualizados com sucesso:', data.mensagem);
                            
                            // Mostra mensagem de sucesso
                            alert('Campos atualizados com sucesso no banco de dados!');
                        } else {
                            console.error('Erro ao atualizar:', data.erro);
                            alert('Erro ao atualizar: ' + data.erro);
                        }
                    })
                    .catch(error => {
                        console.error('Erro na requisição:', error);
                        alert('Erro na comunicação com o servidor: ' + error.message);
                    })
                    .finally(() => {
                        // Fecha o modal
                        var modal = bootstrap.Modal.getInstance(document.getElementById('editEquipModal'));
                        modal.hide();
                    });
                }
            }
        }
    }
}); 