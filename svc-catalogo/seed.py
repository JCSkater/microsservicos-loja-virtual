from flask import Flask
import os
from app.models import db, Produto
from app import create_app

def semear_banco():
    """
    Script de automação para criar as tabelas no SQLite local
    e injetar os produtos iniciais na base de dados catalogo.db.
    """
    app = create_app()
    
    with app.app_context():
        print("🔨 Criando tabelas no banco de dados SQLite...")
        # Cria fisicamente o arquivo .db e as tabelas mapeadas nos models se não existirem
        db.create_all()
        
        # Verifica se o banco já foi semeado anteriormente para evitar duplicidade
        if Produto.query.first() is not None:
            print("✨ O banco de dados já possui produtos cadastrados. Pulando inserção.")
            return

        print("📦 Injetando produtos gamers de teste...")
        produtos_iniciais = [
            Produto(
                id=101,
                nome="Teclado Mecânico RGB",
                descricao="Switches azuis e retroiluminação customizável.",
                preco=299.90,
                imagem_url="images/teclado.jpg",
                estoque=15
            ),
            Produto(
                id=102,
                nome="Mouse Gamer Pro",
                descricao="Sensor óptico de 16000 DPI e 6 botões programáveis.",
                preco=149.90,
                imagem_url="images/mouse.jpg",
                estoque=8
            ),
            Produto(
                id=103,
                nome="Headset Surround 7.1",
                descricao="Almofadas confortáveis e microfone com cancelamento de ruído.",
                preco=249.90,
                imagem_url="images/headset.jpg",
                estoque=20
            )
        ]
        
        # Adiciona e confirma as alterações no banco de dados local
        db.session.bulk_save_objects(produtos_iniciais)
        db.session.commit()
        print("✅ Banco de dados do catálogo semeado com sucesso com 3 produtos!")

if __name__ == "__main__":
    semear_banco()
