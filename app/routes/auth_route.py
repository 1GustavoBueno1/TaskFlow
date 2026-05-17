from flask.blueprints import Blueprint
from flask import request, jsonify, session, Response, render_template, redirect, flash, url_for
from app.services.auth_service import Autenticacao
from app.models.user import UserRepository

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
autenticacao = Autenticacao()
banco = UserRepository()


@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastrar_usuario() -> tuple[Response, int]:
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not nome or not email or not senha:
            flash("Não pode haver campos em branco", "Erro")
            return redirect(url_for('auth.cadastrar_usuario'))
        resposta, mensagem = autenticacao.cadastrar_usuario(nome, email, senha)
        if not resposta:
            flash(mensagem, "Erro")
            return redirect(url_for('auth.cadastrar_usuario'))
        flash(mensagem, "Sucesso")
        return redirect(url_for('auth.login'))
    return render_template('registro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> tuple[Response, int]:
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if not email or not senha:
            flash("Não pode haver campos em branco", "Erro")
            redirect(url_for('auth.login'))
        usuario, mensagem = autenticacao.login(email, senha)
        if usuario is None:
            flash(mensagem, "Erro")
            return redirect(url_for('auth.login'))
        session['user_id'] = usuario.get('id')
        return redirect(url_for('homepage'))
    return render_template('login.html')
