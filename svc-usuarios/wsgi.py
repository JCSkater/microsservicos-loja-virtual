from app import create_app
from app.models import db

# 1. Instancia o servidor Flask de Usuários
application = create_app()

# 2. Contexto de Inicialização de Infraestrutura
# Garante que o SQLAlchemy crie o arquivo usuarios.db e as tabelas vazias 
# dentro do diretório protegido do contêiner antes do servidor começar a rodar
with application.app_context():
    db.create_all()

if __name__ == "__main__":
    # Fallback para execução local de teste
    application.run(host="0.0.0.0", port=5002)
