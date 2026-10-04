from app import create_app

# Instancia a aplicação Flask configurada com as rotas de usuários e Bcrypt
application = create_app()

if __name__ == "__main__":
    # Fallback para execução local de teste
    application.run(host="0.0.0.0", port=5002)
