from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, nullable=False)  # Alinhado com o OpenAPI
    status = db.Column(db.String(30), default='Aguardando Pagamento')  # Status padrão conforme contrato
    valor_total = db.Column(db.Float, nullable=False, default=0.0)
    metodo_pagamento_tipo = db.Column(db.String(50), nullable=False)
    token_simulado = db.Column(db.String(100), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relacionamento com os itens
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True, cascade="all, delete-orphan")

class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido'), nullable=False)
    id_produto = db.Column(db.Integer, nullable=False)  # Alinhado com o OpenAPI
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Float, nullable=False)
