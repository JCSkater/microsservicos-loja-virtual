from flask import Blueprint, jsonify, abort
from app.models import Produto

# Criação do Blueprint do Catálogo
# O prefixo garante que todas as rotas definidas aqui comecem com /api
catalogo_bp = Blueprint('catalogo', __name__, url_prefix='/api')

@catalogo_bp.route('/produtos', methods=['GET'])
def listar_produtos():
    """
    Retorna a lista completa de produtos em formato JSON.
    Alinhado com o status HTTP 200 e 500 do Swagger.
    """
    try:
        # Busca todos os produtos usando a ORM SQLAlchemy
        produtos = Produto.query.all()
        
        # Converte a lista de objetos do banco em dicionários JSON usando o método to_dict()
        return jsonify([produto.to_dict() for produto in produtos]), 200
        
    except Exception as e:
        # AppSec Log: Em produção, registre o erro detalhado internamente (ex: sys.stderr)
        # mas nunca devolva o stack trace completo para o cliente para evitar Information Disclosure.
        return jsonify({"erro": "Falha interna ao acessar a base de dados do catálogo."}), 500

@catalogo_bp.route('/produtos/<int:id>', methods=['GET'])
def buscar_produto(id):
    """
    Busca um único produto com base no ID fornecido na URL.
    Alinhado com as respostas 200, 404 e 500 do Swagger.
    """
    try:
        produto = Produto.query.get(id)
        
        # Validação AppSec / Regra de Negócio: Se o produto não existir, retorna 404 de forma limpa
        if not produto:
            return jsonify({"erro": f"Produto com ID {id} não encontrado."}), 404
            
        return jsonify(produto.to_dict()), 200
        
    except Exception as e:
        return jsonify({"erro": "Erro inesperado ao processar a busca do produto."}), 500
