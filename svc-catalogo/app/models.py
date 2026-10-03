from flask_sqlalchemy import SQLAlchemy

# Inicializa a extensão do banco de dados (SQLAlchemy)
# Ela será vinculada ao Flask no arquivo __init__.py posteriormente
db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = 'produtos'  # Define explicitamente o nome da tabela física

    # Definição das Colunas e Tipos de Dados
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Numeric, nullable=False)
    imagem_url = db.Column(db.String(255), nullable=True)
    estoque = db.Column(db.Integer, nullable=False, default=0)

    def to_dict(self):
        """
        Método auxiliar de serialização.
        Como o Flask não consegue responder um objeto Python puro diretamente,
        convertemos as propriedades do produto em um Dicionário nativo do Python,
        facilitando a transformação final para o formato JSON exigido pelo Swagger.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "imagem_url": self.imagem_url,
            "estoque": self.estoque
        }
