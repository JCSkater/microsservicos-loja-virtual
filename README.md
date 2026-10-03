# 🛍️ Lab: Microsserviços Loja Virtual

Este é um projeto de laboratório prático focado no estudo e implementação de uma **Arquitetura de Microsserviços** e práticas de **DevOps/GitOps**, cobrindo todas as fases do ciclo de vida de desenvolvimento de software (**SDLC**).

O sistema simula o fluxo principal de uma loja virtual (Happy Path de compra), operando de forma **100% local e segura** através de contêineres Docker e emulação de serviços em nuvem.

---

## 🏗️ Arquitetura do Sistema

O projeto é dividido em microsserviços especializados e independentes, que se comunicam de forma sínbria (HTTP/REST) e assíncrona (Mensageria/Event-Driven):

*   **Front-end**: Interface estática simples (HTML, CSS e JavaScript) para interação com o usuário.
*   **API Gateway (Nginx)**: Ponto de entrada único que centraliza as requisições do Front-end e as redireciona para os microsserviços corretos.
*   **svc-usuarios**: Gerencia o cadastro e autenticação de clientes utilizando banco de dados isolado (`usuarios.db`).
*   **svc-catalogo**: Disponibiliza a listagem de produtos através do banco (`catalogo.db`).
*   **svc-pedidos**: Recebe a intenção de compra, persiste o pedido em estado inicial (`pedidos.db`) e dispara eventos de faturamento de forma assíncrona.
*   **svc-pagamentos**: Um worker assíncrono que consome mensagens da fila, processa e simula a aprovação financeira salvando o histórico em (`pagamentos.db`).

---

## 🛠️ Tecnologias Utilizadas

*   **Linguagem & Framework**: Python com Flask (Back-end)
*   **Interface**: HTML5, CSS3 e JavaScript Puro (Front-end)
*   **Banco de Dados**: SQLite (Independente por serviço - *Database-per-Service*)
*   **Mensageria**: AWS SQS (Simulado localmente)
*   **Infraestrutura como Código (IaC)**: Terraform
*   **Ambiente Local & Emulação**: Docker, Docker Compose e LocalStack
*   **CI/CD (Integração Contínua)**: GitHub Actions

---

## 🔄 Fluxo de Integração (SDLC & CI/CD)

A esteira de automação do projeto foi desenhada para garantir a qualidade do software seguindo a cultura DevOps:

1. **Desenvolvimento Local**: O código é escrito no VS Code. O ambiente de infraestrutura (Fila SQS) é criado localmente pelo **Terraform** apontando para o **LocalStack**. Os microsserviços rodam isolados via **Docker Compose**.
2. **Integração Contínua (CI)**: A cada `git push` para o GitHub, o **GitHub Actions** (`ci.yml`) cria uma máquina virtual temporária para:
    * Validar a sintaxe dos arquivos do Terraform (`terraform validate`).
    * Rodar testes automatizados do Python com `pytest`.
    * Garantir que novas alterações não quebrem o ecossistema.

---

## 📂 Estrutura de Pastas do Projeto

```text
microsservicos-loja-virtual/
├── .github/workflows/
│   └── ci.yml               # Pipeline do GitHub Actions (Testes e Validações)
├── terraform/
│   ├── main.tf                  # Criação da fila SQS local no LocalStack
│   ├── variables.tf
│   └── outputs.tf
├── frontend/                # Interface do usuário (HTML/CSS/JS)
├── gateway/                 # API Gateway (Nginx para roteamento das portas)
├── svc-usuarios/            # Microsserviço de Autenticação e Clientes (Flask + SQLite)
├── svc-catalogo/            # Microsserviço de Produtos (Flask + SQLite)
├── svc-pedidos/             # Microsserviço de Pedidos (Flask + SQLite + Envio SQS)
├── svc-pagamentos/          # Worker de Pagamentos (Consumidor SQS + SQLite)
└── docker-compose.yml       # Orquestrador de contêineres locais
```

---

## 🚀 Como Executar o Laboratório (Em Breve)

*Instruções detalhadas de inicialização do Docker Compose e comandos do Terraform serão adicionadas durante as fases de Implementação e Implantação do ciclo SDLC.*
