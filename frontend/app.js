// 🛒 1. ESTADO DA APLICAÇÃO (Memória do Carrinho)
let carrinho = [];
let produtosDoBanco = []; // Substitui a massa estática. Guardará o que vier da API.

// 🎯 2. CAPTURA DOS ELEMENTOS DA TELA
const listaProdutosContainer = document.getElementById('lista-produtos');
const itensCarrinhoContainer = document.getElementById('itens-carrinho');
const valorTotalContador = document.getElementById('valor-total-carrinho');
const btnFinalizar = document.getElementById('btn-finalizar-compra');

// 🔄 3. FUNÇÃO PARA RENDERIZAR A VITRINE DE PRODUTOS DINAMICAMENTE
function renderizarVitrine(produtos) {
    listaProdutosContainer.innerHTML = '';

    produtos.forEach(produto => {
        const produtoCard = document.createElement('div');
        produtoCard.classList.add('produto-card');

        produtoCard.innerHTML = `
            <img src="${produto.imagem_url}" alt="${produto.nome}" style="max-width:120px; border-radius:4px;">
            <h3>${produto.nome}</h3>
            <p style="font-size: 0.9rem; color: #64748b;">${produto.descricao}</p>
            <div class="produto-preco">R$ ${Number(produto.preco || 0).toFixed(2)}</div>
            <p style="font-size: 0.8rem;">Estoque: ${produto.estoque} un</p>
            <button onclick="adicionarAoCarrinho(${produto.id})">Adicionar ao Carrinho</button>
        `;

        listaProdutosContainer.appendChild(produtoCard);
    });
}

// ➕ 4. FUNÇÃO PARA ADICIONAR O PRODUTO NO ARRANGEMENT DO CARRINHO
window.adicionarAoCarrinho = function(idProduto) {
    // Busca o produto na lista que veio do banco de dados real
    const produtoEncontrado = produtosDoBanco.find(p => p.id === idProduto);
    
    if (!produtoEncontrado) return;

    const itemNoCarrinho = carrinho.find(item => item.id === idProduto);

    if (itemNoCarrinho) {
        itemNoCarrinho.quantidade += 1;
    } else {
        carrinho.push({
            id: produtoEncontrado.id,
            nome: produtoEncontrado.nome,
            preco: produtoEncontrado.preco,
            quantidade: 1
        });
    }

    atualizarInterfaceCarrinho();
};

// 🔄 5. FUNÇÃO PARA ATUALIZAR A INTERFACE DO CARRINHO E VALOR TOTAL
function atualizarInterfaceCarrinho() {
    if (carrinho.length === 0) {
        itensCarrinhoContainer.innerHTML = '<li class="vazio">Seu carrinho está vazio.</li>';
        valorTotalContador.innerText = '0.00';
        btnFinalizar.disabled = true;
        return;
    }

    itensCarrinhoContainer.innerHTML = '';
    let totalAcumulado = 0;

    carrinho.forEach(item => {
        // Garantindo que o preço seja tratado como número para o cálculo de subtotal
        const precoNumerico = Number(item.preco || 0);
        const subtotal = precoNumerico * item.quantidade;
        totalAcumulado += subtotal;

        const li = document.createElement('li');
        li.style.padding = '0.5rem 0';
        li.style.borderBottom = '1px solid #cbd5e1';
        li.style.display = 'flex';
        li.style.justifyContent = 'space-between';
        
        // Correção aplicada usando Number().toFixed(2) para blindar a exibição
        li.innerHTML = `
            <div>
                <strong>${item.nome}</strong><br>
                <small>${item.quantidade}x R$ ${precoNumerico.toFixed(2)}</small>
            </div>
            <span>R$ ${subtotal.toFixed(2)}</span>
        `;
        
        itensCarrinhoContainer.appendChild(li);
    });

    valorTotalContador.innerText = totalAcumulado.toFixed(2);
    btnFinalizar.disabled = false;
}


// 🚀 6. EVENTO DO BOTÃO FINALIZAR COMPRA
btnFinalizar.addEventListener('click', () => {
    alert(`Sucesso! Pedido fechado no valor de R$ ${valorTotalContador.innerText}.\n\n[Simulação]: Payload pronto para o svc-pedidos!`);
    carrinho = [];
    atualizarInterfaceCarrinho();
});

// 🚀 CONSUMO REAL DA INFRAESTRUTURA DOCKER (CONEXÃO COM O GATEWAY NGINX)
function carregarProdutosDoCatalogo() {
    fetch('http://127.0.0.1:8080/api/produtos')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(dadosDoBanco => {
            produtosDoBanco = dadosDoBanco;
            renderizarVitrine(produtosDoBanco);
        })
        .catch(erro => {
            console.error("Falha ao conectar no API Gateway:", erro);
            listaProdutosContainer.innerHTML = `
                <p class="carregando" style="color: #dc2626;">
                    ❌ Erro de Conexão: Não foi possível carregar a vitrine através do API Gateway. 
                    Verifique se o contêiner 'loja-gateway' está rodando na porta 8080.
                </p>
            `;
        });
}

// Inicializa a carga de dados assim que a página abre
carregarProdutosDoCatalogo();
