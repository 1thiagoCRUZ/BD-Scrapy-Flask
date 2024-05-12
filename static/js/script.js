document.getElementById('bancoForm').addEventListener('submit', async function(event){
    event.preventDefault();

    var formData = new FormData(document.getElementById('bancoForm'));
    var nomeBanco = formData.get('nome').toLowerCase();

    try {
        var response = await fetch('/buscar', {
            method: 'POST',
            body: new URLSearchParams({
                'nome': nomeBanco
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        var linhas = await response.json();

        var divTabela = document.getElementById('table');
        for (var linha of linhas) {
            var novaLinha = document.createElement('div');
            novaLinha.classList.add('table-row');
            novaLinha.innerHTML = `
                <div class="table-cell">${linha.nome}</div>
                <div class="table-cell">${linha.data_publicacao}</div>
                <div class="table-cell">${linha.lucro_liquido}</div>
                <div class="table-cell">${linha.patrimonio_liquido}</div>
                <div class="table-cell">${linha.ativo_total}</div>
                <div class="table-cell">${linha.captacoes}</div>
                <div class="table-cell">${linha.carteira_credito_classificada}</div>
                <div class="table-cell">${linha.patrimonio_referencia_rwa}</div>
                <div class="table-cell">${linha.numero_agencias}</div>
                <div class="table-cell">${linha.numero_pontos_atendimento}</div>
            `;
            divTabela.appendChild(novaLinha);
        }
    } catch (error) {
        alert("Erro ao buscar dados do banco");
    }
})
