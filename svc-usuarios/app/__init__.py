import os
from flask import Flask
from app.models import db, bcrypt

def create_app():
    """
    Factory Function: Instancia, configura e blinda o microsserviço de Usuários.
    """
    app = Flask(__name__)

    # Configuração de AppSec: Isolamento do banco de dados usuários.db
    # Usamos o caminho absoluto dentro da pasta /app/data protegida do contêiner
    database_url = os.getenv("DATABASE_URL", "sqlite:////app/data/usuarios.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa as extensões vinculando-as a esta instância do Flask
    db.init_app(app)
    bcrypt.init_app(app)  # 🔒 Ativa o Bcrypt no ecossistema do app

    # Nota de AppSec: Como centralizamos o gerenciamento de CORS no Nginx Gateway,
    # não há necessidade de declarar flask_cors aqui. O gateway cuidará disso na borda.

    # =======================================================================
    # REGISTRO DAS ROTAS DE AUTENTICAÇÃO (VINCULADO AO ROUTES.PY)
    # =======================================================================
    from app.routes import usuarios_bp
    app.register_blueprint(usuarios_bp)

    # Rota de Health Check para monitoramento e DevOps SRE
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "UP", "servico": "svc-usuarios"}, 200

    return app
