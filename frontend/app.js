// 📦 1. MASSA DE DADOS SIMULADA (MOCK)
const produtosSimulados = [
    {
        id: 101,
        nome: "Teclado Mecânico RGB",
        descricao: "Switches azuis e retroiluminação customizável.",
        preco: 299.90,
        imagem_url: "images/teclado.jpg",
        estoque: 15
    },
    {
        id: 102,
        nome: "Mouse Gamer Pro",
        descricao: "Sensor óptico de 16000 DPI e 6 botões programáveis.",
        preco: 149.90,
        imagem_url: "images/mouse.jpg",
        estoque: 8
    },
    {
        id: 103,
        nome: "Headset Surround 7.1",
        descricao: "Almofadas confortáveis e microfone com cancelamento de ruído.",
        preco: 249.90,
        imagem_url: "images/headset.jpg",
        estoque: 20
    }
];

// 🛒 2. ESTADO DA APLICAÇÃO (Memória do Carrinho)
let carrinho = [];

// 🎯 3. CAPTURA DOS ELEMENTOS DA TELA
const listaProdutosContainer = document.getElementById('lista-produtos');
const itensCarrinhoContainer = document.getElementById('itens-carrinho');
const valorTotalContador = document.getElementById('valor-total-carrinho');
const btnFinalizar = document.getElementById('btn-finalizar-compra');

// 🔄 4. FUNÇÃO PARA RENDERIZAR A VITRINE DE PRODUTOS
function renderizarVitrine(produtos) {
    listaProdutosContainer.innerHTML = '';

    produtos.forEach(produto => {
        const produtoCard = document.createElement('div');
        produtoCard.classList.add('produto-card');

        produtoCard.innerHTML = `
            <img src="${produto.imagem_url}" alt="${produto.nome}" style="max-width:120px; border-radius:4px;">
            <h3>${produto.nome}</h3>
            <p style="font-size: 0.9rem; color: #64748b;">${produto.descricao}</p>
            <div class="produto-preco">R$ ${produto.preco.toFixed(2)}</div>
            <p style="font-size: 0.8rem;">Estoque: ${produto.estoque} un</p>
            <button onclick="adicionarAoCarrinho(${produto.id})">Adicionar ao Carrinho</button>
        `;

        listaProdutosContainer.appendChild(produtoCard);
    });
}

// ➕ 5. FUNÇÃO PARA ADICIONAR O PRODUTO NO ARRANGEMENT DO CARRINHO
window.adicionarAoCarrinho = function(idProduto) {
    const produtoEncontrado = produtosSimulados.find(p => p.id === idProduto);
    
    if (!produtoEncontrado) return;

    // Verifica se o item já existe no carrinho
    const itemNoCarrinho = carrinho.find(item => item.id === idProduto);

    if (itemNoCarrinho) {
        // Se já existe, apenas aumenta a quantidade comprada
        itemNoCarrinho.quantidade += 1;
    } else {
        // Se é a primeira vez, adiciona o objeto com quantidade inicial 1
        carrinho.push({
            id: produtoEncontrado.id,
            nome: produtoEncontrado.nome,
            preco: produtoEncontrado.preco,
            quantidade: 1
        });
    }

    // Atualiza a interface gráfica do carrinho
    atualizarInterfaceCarrinho();
};

// 🔄 6. FUNÇÃO PARA ATUALIZAR A INTERFACE DO CARRINHO E VALOR TOTAL
function atualizarInterfaceCarrinho() {
    // Se o carrinho estiver vazio, exibe a mensagem padrão
    if (carrinho.length === 0) {
        itensCarrinhoContainer.innerHTML = '<li class="vazio">Seu carrinho está vazio.</li>';
        valorTotalContador.innerText = '0.00';
        btnFinalizar.disabled = true;
        return;
    }

    // Caso contrário, limpa o container e renderiza a lista atualizada
    itensCarrinhoContainer.innerHTML = '';
    let totalAcumulado = 0;

    carrinho.forEach(item => {
        const subtotal = item.preco * item.quantidade;
        totalAcumulado += subtotal;

        const li = document.createElement('li');
        li.style.padding = '0.5rem 0';
        li.style.borderBottom = '1px solid #cbd5e1';
        li.style.display = 'flex';
        li.style.justifyContent = 'space-between';
        
        li.innerHTML = `
            <div>
                <strong>${item.nome}</strong><br>
                <small>${item.quantidade}x R$ ${item.preco.toFixed(2)}</small>
            </div>
            <span>R$ ${subtotal.toFixed(2)}</span>
        `;
        
        itensCarrinhoContainer.appendChild(li);
    });

    // Atualiza o valor total impresso e habilita o botão de finalizar
    valorTotalContador.innerText = totalAcumulado.toFixed(2);
    btnFinalizar.disabled = false;
}

// 🚀 7. EVENTO DO BOTÃO FINALIZAR COMPRA (Simulação de Mensageria)
btnFinalizar.addEventListener('click', () => {
    alert(`Sucesso! Seu pedido com ${carrinho.length} tipo(s) de produto(s) foi fechado no valor de R$ ${valorTotalContador.innerText}.\n\n[Simulação DevOps]: Payload JSON gerado e pronto para envio via POST para o svc-pedidos!`);
    
    // Limpa o carrinho após finalizar a compra fictícia
    carrinho = [];
    atualizarInterfaceCarrinho();
});

// 🚀 8. INICIALIZAÇÃO
setTimeout(() => {
    renderizarVitrine(produtosSimulados);
}, 500);
