from flask.blueprints import Blueprint
from app.services.auth_service import Auth
from flask import request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register_user() -> tuple[bool, str]:
    if request.method == 'POST':
        auth = Auth()
        dados = request.get_json()
        if not dados:
            return jsonify({"erro": "Body json e obrigatorio"}), 400
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('password')
        if not nome or not email or not senha:
            return jsonify({"erro": "Todos os campos devem estar preenchidos"}), 400
        reposta, mensagem = auth.register_user(nome, email, senha)
        if not reposta:
            return jsonify({"erro": mensagem}), 400
        return jsonify({"Sucesso": mensagem}), 201
@auth_bp.route('/login', methods = ['GET', 'POST'])
def login() -> tuple[bool, str]:
    if request.method == 'POST':
        ...
