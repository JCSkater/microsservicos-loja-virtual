from flask import Blueprint, request, jsonify
from app.models import db, Usuario

# Criação do Blueprint de Usuários com o prefixo /api
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')

@usuarios_bp.route('/register', methods=['POST'])
def registrar_usuario():
    """
    Endpoint para cadastro de novos clientes.
    Hashea a senha e valida a unicidade do email/cpf.
    """
    try:
        dados = request.get_json()
        
        # 1. Validação Defensiva Básica (Input Validation)
        campos_obrigatorios = ["nome", "email", "senha", "cpf", "endereco"]
        for campo in campos_obrigatorios:
            if not dados or campo not in dados or not str(dados[campo]).strip():
                return jsonify({"erro": f"O campo '{campo}' é obrigatório."}), 400

        email = dados["email"].strip().lower()
        cpf = "".join(filter(str.isdigit, str(dados["cpf"]))) # Sanitiza CPF (apenas números)

        # 2. Verificação de Duplicidade (Prevenção de Abuso)
        if Usuario.query.filter((Usuario.email == email) | (Usuario.cpf == cpf)).first():
            return jsonify({"erro": "Email ou CPF já cadastrados no sistema."}), 409

        # 3. Criação do Registro Seguro
        novo_usuario = Usuario(
            nome=dados["nome"].strip(),
            email=email,
            cpf=cpf,
            endereco=dados["endereco"].strip()
        )
        # Invoca o método do model que gera o hash Bcrypt robusto
        novo_usuario.set_senha(dados["senha"])

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"mensagem": "Usuário cadastrado com sucesso!", "usuario_id": novo_usuario.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Falha interna ao processar o cadastro."}), 500


@usuarios_bp.route('/login', methods=['POST'])
def login_usuario():
    """
    Endpoint para autenticação de clientes.
    AppSec: Mensagem de erro genérica evita enumeração de contas (Username Enumeration).
    """
    try:
        dados = request.get_json()
        
        if not dados or "email" not in dados or "senha" not in dados:
            return jsonify({"erro": "Email e senha são obrigatórios."}), 400

        email = dados["email"].strip().lower()
        senha = dados["senha"]

        # Busca o usuário pelo e-mail
        usuario = Usuario.query.filter_by(email=email).first()

        # AppSec: Se o usuário não existir OU a senha estiver errada,
        # retornamos a MESMA mensagem genérica 401 (Não Autorizado).
        # Se dissermos "Senha incorreta", um atacante saberá que o email existe no banco.
        if not usuario or not usuario.check_senha(senha):
            return jsonify({"erro": "Credenciais inválidas. Verifique seu e-mail e/ou senha."}), 401

        # Autenticação Funcional Simplificada para o Lab
        # Em produção, aqui geraríamos um JWT (JSON Web Token) assinado.
        return jsonify({
            "mensagem": "Autenticação bem-sucedida!",
            "usuario": usuario.to_dict() # Retorna o dicionário sem o hash da senha
        }), 200

    except Exception as e:
        return jsonify({"erro": "Falha interna ao processar o login."}), 500
