from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # Referência ao ID do svc-usuarios
    status = db.Column(db.String(20), default='PENDENTE')  # PENDENTE, PAGO, CANCELADO
    total = db.Column(db.Float, nullable=False, default=0.0)
    criado_em = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamento com os itens do pedido
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade="all, delete-orphan")

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    produto_id = db.Column(db.Integer, nullable=False)  # Referência ao ID do svc-catalogo
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)
