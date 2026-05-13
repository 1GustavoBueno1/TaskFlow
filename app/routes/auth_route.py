from flask.blueprints import Blueprint
from app.services.auth_service import Auth
from app.models.user import UserRepository
from flask import request, jsonify, session

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')
auth = Auth()
db = UserRepository()
@auth_bp.route('/register', methods = ['POST'])
def register_user() -> tuple[bool, str]:
    if request.method == 'POST':
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
@auth_bp.route('/login', methods = ['POST'])
def login() -> tuple[bool, str]:
    if request.method == 'POST':
        dados_do_usuario = request.get_json()
        if not dados_do_usuario:
            return jsonify({"Erro": "Body json e obrigatorio!"}), 400
        email = dados_do_usuario.get('email')
        senha = dados_do_usuario.get('senha')
        if not email or not senha:
            return jsonify({"Erro": "Todos os campos devem estar preenchidos!"}), 400
        user, msg = auth.login(email, senha)
        if user is None:
            return jsonify({"Erro": msg}), 401
        user_id = user.get('id')
        session['user_id'] = user_id
        return jsonify({"Sucesso": msg, "user": user_id}), 200
