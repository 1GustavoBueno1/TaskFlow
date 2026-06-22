from flask.blueprints import Blueprint
from flask import request, session, Response, render_template, redirect, url_for, flash
from app.models.user import UserRepository
from app.services.auth_service import Autenticacao
from app.services.user_service import Usuario
from app.decorators import login_necessario
usuario_bp = Blueprint('usuario', __name__, url_prefix='/perfil')
banco_usuario = UserRepository()
servico_usuario = Usuario()
servico_auth = Autenticacao()
@usuario_bp.route('/visualizar', methods=['GET'])
@login_necessario
def visualizar_perfil() -> Response | str:
    id_usuario = session.get('user_id')
    usuario = banco_usuario.find(id_usuario)
    return render_template('perfil.html', dados_do_perfil = usuario)


@usuario_bp.route('/editar/<coluna>', methods=['GET', 'POST'])
@login_necessario
def editar_perfil(coluna) -> str | Response:
    id_usuario = session.get('user_id')
    novo_dado = request.form.get(coluna)
    user_senha = request.form.get('password1')
    usuario = banco_usuario.find(id_usuario)
    resposta, mensagem = servico_usuario.editar_perfil(coluna, novo_dado, user_senha, id_usuario, usuario)
    if resposta:
        flash(mensagem, 'sucesso')
        return redirect(url_for('usuario.visualizar_perfil'))
    return render_template('edit_user.html', coluna = coluna)
@usuario_bp.route('/sair', methods = ['GET', 'POST'])
@login_necessario
def sair() -> Response | str:
    id_usuario = session.get('user_id')
    if request.method == 'POST':
        senha_user = request.form.get('password')
        usuario = banco_usuario.find(id_usuario)
        resposta, mensagem = servico_auth.sair(senha_user, usuario)
        if resposta:
            session.clear()
            flash(mensagem, 'sucesso')
            return redirect(url_for('homepage'))
        flash(mensagem, 'erro')
        return redirect(url_for('usuario.visualizar_perfil'))
    return render_template('logout.html')
