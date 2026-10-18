from flask import Flask, request, jsonify
from app.models import db, Pedido, ItemPedido

def create_app():
    app = Flask(__name__)
    
    # Configuração do banco de dados SQLite local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../pedidos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    # Cria as tabelas caso não existam
    with app.app_context():
        db.create_all()

    # Rota: Criar um novo pedido
    @app.route('/pedidos', methods=['POST'])
    def criar_pedido():
        dados = request.get_json()
        
        if not dados or 'usuario_id' not in dados or 'itens' not in dados:
            return jsonify({'erro': 'Dados incompletos'}), 400
            
        try:
            novo_pedido = Pedido(usuario_id=dados['usuario_id'], total=0.0)
            db.session.add(novo_pedido)
            db.session.flush() # Gera o ID do pedido antes do commit definitivo
            
            valor_total = 0.0
            for item in dados['itens']:
                subtotal = item['quantidade'] * item['preco_unitario']
                valor_total += subtotal
                
                novo_item = ItemPedido(
                    pedido_id=novo_pedido.id,
                    produto_id=item['produto_id'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario']
                )
                db.session.add(novo_item)
            
            novo_pedido.total = valor_total
            db.session.commit()
            
            return jsonify({'mensagem': 'Pedido criado com sucesso', 'pedido_id': novo_pedido.id}), 210
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': str(e)}), 500

    # Rota: Listar todos os pedidos
    @app.route('/pedidos', methods=['GET'])
    def listar_pedidos():
        pedidos = Pedido.query.all()
        resultado = []
        for p in pedidos:
            itens_lista = [{
                'produto_id': i.produto_id,
                'quantidade': i.quantidade,
                'preco_unitario': i.preco_unitario
            } for i in p.itens]
            
            resultado.append({
                'id': p.id,
                'usuario_id': p.usuario_id,
                'status': p.status,
                'total': p.total,
                'criado_em': p.criado_em.strftime('%Y-%m-%d %H:%M:%S'),
                'itens': itens_lista
            })
        return jsonify(resultado), 200

    return app
