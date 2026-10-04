from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Usuario(db.Model):
    """
    Mapeamento da tabela 'usuarios' no banco usuarios.db.
    Aplica controles estritos de integridade de dados e hashing de credenciais.
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # AppSec: Email e CPF como chaves únicas evitam ataques de duplicação de contas
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    
    # Campo para armazenar o hash seguro da senha (nunca o texto claro)
    # O hash do Bcrypt geralmente possui 60 caracteres, limitamos em 255 por segurança
    senha_hash = db.Column(db.String(255), nullable=False)
    
    endereco = db.Column(db.String(255), nullable=False)

    def set_senha(self, senha_puro_texto):
        """
        Gera o hash seguro da senha usando Bcrypt e armazena no modelo.
        Aplica automaticamente o Salt e o Fator de Custo.
        """
        # decode('utf-8') é necessário porque o bcrypt gera uma string de bytes,
        # e o banco de dados precisa receber uma string de texto comum.
        self.senha_hash = bcrypt.generate_password_hash(senha_puro_texto).decode('utf-8')

    def check_senha(self, senha_puro_texto):
        """
        Valida se a senha digitada no login confere com o hash salvo no banco.
        Retorna True se estiver correta, ou False se falhar.
        """
        return bcrypt.check_password_hash(self.senha_hash, senha_puro_texto)

    def to_dict(self):
        """
        Serializa os dados para resposta JSON da API.
        AppSec: O campo 'senha_hash' NUNCA deve ser incluído aqui para evitar Data Exposure.
        """
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cpf": self.cpf,
            "endereco": self.endereco
        }
