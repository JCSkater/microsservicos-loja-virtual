import os
from flask import Flask
from flask_cors import CORS
from app.models import db

def create_app():
    """
    Factory Function: Cria e configura a instância do servidor Flask.
    """
    app = Flask(__name__)

    # Configuração do banco de dados vinda do ambiente
    database_url = os.getenv("DATABASE_URL", "sqlite:///catalogo.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa o banco de dados vinculando-o ao Flask
    db.init_app(app)

    # Configuração de CORS restringindo o tráfego local
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost", "http://127.0.0.1"]}})

    # ==========================================
    # REGISTRO DAS ROTAS (PADRÃO DE MERCADO)
    # ==========================================
    from app.routes import catalogo_bp
    app.register_blueprint(catalogo_bp)

    # Rota básica de monitoramento (Health Check)
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "UP", "servico": "svc-catalogo"}, 200

    return app
