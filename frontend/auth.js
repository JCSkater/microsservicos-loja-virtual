// Captura os botões das abas (Login e Cadastro)
const btnAbaLogin = document.getElementById('btn-aba-login');
const btnAbaCadastro = document.getElementById('btn-aba-cadastro');

// Captura os dois formulários físicos da tela
const formLogin = document.getElementById('form-login');
const formCadastro = document.getElementById('form-cadastro');

// Evento quando o usuário clica na aba "Cadastro"
btnAbaCadastro.addEventListener('click', () => {
    // Ajusta o visual dos botões de aba
    btnAbaCadastro.classList.add('ativo');
    btnAbaLogin.classList.remove('ativo');

    // Mostra o formulário de cadastro e esconde o de login
    formCadastro.classList.remove('escondido');
    formLogin.classList.add('escondido');
});

// Evento quando o usuário clica na aba "Login"
btnAbaLogin.addEventListener('click', () => {
    // Ajusta o visual dos botões de aba
    btnAbaLogin.classList.add('ativo');
    btnAbaCadastro.classList.remove('ativo');

    // Mostra o formulário de login e esconde o de cadastro
    formLogin.classList.remove('escondido');
    formCadastro.classList.add('escondido');
});

// Captura o envio do formulário de Cadastro (Simulação de Sucesso)
formCadastro.addEventListener('submit', (event) => {
    event.preventDefault(); // Impede a página de recarregar
    alert('Simulação AppSec: Conta cadastrada com sucesso locais! Dados validados.');
    // Futuramente aqui faremos o fetch() POST para o seu svc-usuarios
    btnAbaLogin.click(); // Redireciona visualmente para o login
});

// Captura o envio do formulário de Login (Simulação de Sucesso)
formLogin.addEventListener('submit', (event) => {
    event.preventDefault();
    alert('Simulação AppSec: Login bem-sucedido! Redirecionando para a loja.');
    // Redireciona o navegador de volta para a Home da loja
    window.location.href = 'index.html';
});
