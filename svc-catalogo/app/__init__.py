import os
from flask import Flask
from app.models import db

def create_app():
    """
    Factory Function: Cria e configura a instância do servidor Flask.
    """
    app = Flask(__name__)

    # Configuração do banco de dados vinda do ambiente
    database_url = os.getenv("DATABASE_URL", "sqlite:////app/data/catalogo.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa o banco de dados vinculando-o ao Flask
    db.init_app(app)

    # =======================================================================
    # NOTA APPSEC: CORS RE-REMOVIDO DAQUI. O API Gateway gerencia isso na borda.
    # =======================================================================

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
