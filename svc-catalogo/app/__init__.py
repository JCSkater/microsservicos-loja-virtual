import os
from flask import Flask
from flask_cors import CORS
from app.models import db

def create_app():
    """
    Factory Function: Cria e configura a instância do servidor Flask.
    """
    app = Flask(__name__)

    # Configuração de AppSec: O caminho do banco de dados vem de uma variável de ambiente.
    # Se ela não existir, ele usa o SQLite local como padrão seguro (fallback).
    database_url = os.getenv("DATABASE_URL", "sqlite:///catalogo.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializa o banco de dados vinculando-o a esta instância do Flask
    db.init_app(app)

    # Configuração de AppSec: Habilita o CORS restringindo as origens permitidas.
    # No desenvolvimento local, liberamos apenas o seu Front-end estático para consultar a API.
    CORS(app, resources={r"/api/*": {"origins": ["http://localhost", "http://127.0.0.1"]}})

    # Aqui no futuro registraremos as rotas (Blueprints)
    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "UP", "servico": "svc-catalogo"}, 200

    return app
