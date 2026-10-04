from app import create_app

# A variável de inicialização do servidor de produção
application = create_app()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5001)
