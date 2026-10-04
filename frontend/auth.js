// 🎯 1. CAPTURA DOS ELEMENTOS DE NAVEGAÇÃO E ABAS
const btnAbaLogin = document.getElementById('btn-aba-login');
const btnAbaCadastro = document.getElementById('btn-aba-cadastro');
const formLogin = document.getElementById('form-login');
const formCadastro = document.getElementById('form-cadastro');

// 🔄 2. MECÂNICA VISUAL DE ALTERNÂNCIA DE ABAS
btnAbaCadastro.addEventListener('click', () => {
    btnAbaCadastro.classList.add('ativo');
    btnAbaLogin.classList.remove('ativo');
    formCadastro.classList.remove('escondido');
    formLogin.classList.add('escondido');
});

btnAbaLogin.addEventListener('click', () => {
    btnAbaLogin.classList.add('ativo');
    btnAbaCadastro.classList.remove('ativo');
    formLogin.classList.remove('escondido');
    formCadastro.classList.add('escondido');
});

// =======================================================================
// 🚀 3. INTEGRAÇÃO REAL: ENVIO DO FORMULÁRIO DE CADASTRO (POST /api/register)
// =======================================================================
formCadastro.addEventListener('submit', (event) => {
    event.preventDefault(); // Impede a página de recarregar

    // Captura os valores digitados no formulário físico do HTML
    const payload = {
        nome: document.getElementById('cad-nome').value,
        email: document.getElementById('cad-email').value,
        senha: document.getElementById('cad-senha').value,
        cpf: document.getElementById('cad-cpf').value,
        endereco: document.getElementById('cad-endereco').value
    };

    // Dispara a requisição POST para a porta do nosso API Gateway (Nginx)
    fetch('http://127.0.0', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        return response.json().then(dados => {
            if (!response.ok) {
                // Captura erros tratados no back-end (ex: campos vazios, CPF duplicado)
                throw new Error(dados.erro || "Falha ao realizar cadastro.");
            }
            return dados;
        });
    })
    .then(sucesso => {
        alert(`✅ ${sucesso.mensagem}`);
        formCadastro.reset(); // Limpa as caixas de texto do formulário
        btnAbaLogin.click();  // Redireciona visualmente o usuário para a aba de Login
    })
    .catch(erro => {
        console.error("Erro no cadastro:", erro);
        alert(`❌ Erro no Cadastro: ${erro.message}`);
    });
});

// =======================================================================
// 🚀 4. INTEGRAÇÃO REAL: ENVIO DO FORMULÁRIO DE LOGIN (POST /api/login)
// =======================================================================
formLogin.addEventListener('submit', (event) => {
    event.preventDefault();

    const payload = {
        email: document.getElementById('login-email').value,
        senha: document.getElementById('login-senha').value
    };

    fetch('http://127.0.0', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        return response.json().then(dados => {
            if (!response.ok) {
                throw new Error(dados.erro || "Falha na autenticação.");
            }
            return dados;
        });
    })
    .then(sucesso => {
        alert("🔒 Autenticação bem-sucedida! Redirecionando para a loja.");
        
        // Simulação de sessão: Guarda os dados do usuário na memória local do navegador (SessionStorage)
        sessionStorage.setItem('usuario_logado', JSON.stringify(sucesso.usuario));
        
        // Redireciona o navegador de volta para a Home da loja virtual
        window.location.href = 'index.html';
    })
    .catch(erro => {
        console.error("Erro no login:", erro);
        alert(`❌ Erro no Login: ${erro.message}`);
    });
});
