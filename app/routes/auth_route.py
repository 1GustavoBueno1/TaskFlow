from flask.blueprints import Blueprint
from flask import request, jsonify, session, Response, render_template, redirect
from app.services.auth_service import Autenticacao
from app.models.user import UserRepository

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
autenticacao = Autenticacao()
banco = UserRepository()


@auth_bp.route('/cadastro', methods=['POST'])
def cadastrar_usuario() -> tuple[Response, int]:
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not nome or not email or not senha:
            return jsonify({"Erro": "Todos os campos devem estar preenchidos"}), 400
        resposta, mensagem = autenticacao.cadastrar_usuario(nome, email, senha)
        if not resposta:
            return jsonify({"Erro": mensagem}), 400
        return jsonify({"Sucesso": mensagem}), 201
    return render_template('registro.html')


@auth_bp.route('/login', methods=['POST'])
def login() -> tuple[Response, int]:
    if request.method == 'POST':
        dados = request.get_json()
        if not dados:
            return jsonify({"Erro": "Body JSON é obrigatório!"}), 400
        email = dados.get('email')
        senha = dados.get('senha')
        if not email or not senha:
            return jsonify({"Erro": "Todos os campos devem estar preenchidos!"}), 400
        usuario, mensagem = autenticacao.login(email, senha)
        if usuario is None:
            return jsonify({"Erro": mensagem}), 401
        session['user_id'] = usuario.get('id')
        return jsonify({"Sucesso": mensagem, "usuario": usuario.get('id')}), 200
