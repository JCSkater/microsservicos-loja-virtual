from flask import Flask, request, jsonify
import requests  # Biblioteca para chamadas HTTP síncronas
from app.models import db, Pedido, ItemPedido

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../pedidos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # URL interna do serviço de usuários dentro da rede Docker (ou localhost para testes locais)
    # Em produção/Docker Compose, o nome do serviço substitui o IP/localhost
    USUARIOS_SERVICE_URL = "http://svc-usuarios:5001/api/usuarios"

    # Rota POST: Criar um novo pedido (Fechar Compra)
    @app.route('/api/pedidos', methods=['POST'])
    def criar_pedido():
        dados = request.get_json()
        
        # Validação básica de campos obrigatórios conforme o openapi.yaml (Sintaxe Corrigida)
        campos_obrigatorios = ['id_usuario', 'valor_total', 'metodo_pagamento', 'itens']
        if not dados or not all(campo in dados for campo in campos_obrigatorios):
            return jsonify({'erro': 'Requisição malformada. Campos obrigatórios ausentes.'}), 400
            
        id_usuario = dados['id_usuario']
        
        # --- VALIDAÇÃO SÍNCRONA VIA HTTP (svc-usuarios) ---
        try:
            url_validacao = f"{USUARIOS_SERVICE_URL}/{id_usuario}"
            resposta_usuarios = requests.get(url_validacao, timeout=3.0)
            
            # Se o serviço de usuários responder 404, o usuário não existe
            if resposta_usuarios.status_code == 404:
                return jsonify({
                    'erro': f'Entidade improcessável. Usuário com ID {id_usuario} não localizado no sistema.'
                }), 422
                
            # Se responder qualquer outro erro diferente de 200 OK
            if resposta_usuarios.status_code != 200:
                return jsonify({
                    'erro': 'Não foi possível validar o usuário no momento. Resposta inválida do serviço de autenticação.'
                }), 502
                
        except requests.exceptions.RequestException as e:
            # Falha de rede, timeout ou serviço svc-usuarios fora do ar
            return jsonify({
                'erro': 'Erro interno do servidor. Falha de comunicação síncrona com svc-usuarios.',
                'detalhes': str(e)
            }), 500
        # --------------------------------------------------

        try:
            valor_total = dados['valor_total']
            metodo = dados['metodo_pagamento']
            
            novo_pedido = Pedido(
                id_usuario=id_usuario,
                valor_total=valor_total,
                status='Aguardando Pagamento',
                metodo_pagamento_tipo=metodo.get('tipo', 'cartao_credito'),
                token_simulado=metodo.get('token_simulado', '')
            )
            db.session.add(novo_pedido)
            db.session.flush()  # Descobre o id_pedido gerado automaticamente
            
            for item in dados['itens']:
                novo_item = ItemPedido(
                    id_pedido=novo_pedido.id_pedido,
                    id_produto=item['id_produto'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario']
                )
                db.session.add(novo_item)
            
            db.session.commit()
            
            # [TODO] Chamar a lógica de queue.py aqui para publicar no SQS do LocalStack
            # publicar_no_sqs(novo_pedido)
            
            return jsonify({
                'id_pedido': novo_pedido.id_pedido,
                'status': novo_pedido.status,
                'mensagem': 'Pedido recebido! Processando o faturamento.'
            }), 201
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'erro': 'Erro interno do servidor', 'detalhes': str(e)}), 500

    # Rota GET: Histórico de pedidos por usuário
    @app.route('/api/pedidos/usuario/<int:id_usuario>', methods=['GET'])
    def listar_pedidos_por_usuario(id_usuario):
        pedidos = Pedido.query.filter_by(id_usuario=id_usuario).all()
        
        if not pedidos:
            return jsonify({'erro': 'Nenhum pedido encontrado para o usuário informado.'}), 404
            
        resultado = []
        for p in pedidos:
            resultado.append({
                'id_pedido': p.id_pedido,
                'valor_total': p.valor_total,
                'status': p.status,
                'data_criacao': p.data_criacao.strftime('%Y-%m-%dT%H:%M:%SZ')
            })
            
        return jsonify(resultado), 200

    return app
