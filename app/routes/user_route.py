from flask.blueprints import Blueprint
from flask import request, session, Response, render_template, redirect, url_for, flash
from app.models.user import UserRepository
from app.services.user_service import Usuario

usuario_bp = Blueprint('usuario', __name__, url_prefix='/perfil')
banco_usuario = UserRepository()
servico_usuario = Usuario()
#Collecting Flask-WTF
@usuario_bp.route('/visualizar', methods=['GET'])
def visualizar_perfil() -> tuple[Response, int]:
    if request.method == 'GET':
        id_usuario = session.get('user_id')
        if id_usuario:
            usuario = banco_usuario.find(id_usuario)
            return render_template('perfil.html', dados_do_perfil = usuario)
        return redirect(url_for('homepage'))


@usuario_bp.route('/editar/<coluna>', methods=['GET', 'POST'])
def editar_perfil(coluna) -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            novo_dado = request.form.get(coluna)
            user_senha = request.form.get('password1')
            usuario = banco_usuario.find(id_usuario)
            resposta, mensagem = servico_usuario.editar_perfil(coluna, novo_dado, user_senha, id_usuario, usuario)
            if resposta:
                flash(mensagem, 'sucesso')
                return redirect(url_for('usuario.visualizar_perfil'))
            flash(mensagem, 'erro')
            return redirect(url_for('usuario.visualizar_perfil'))
        flash("efetue login para prosseguir", 'erro')
        return redirect(url_for('homepage'))
    return render_template('edit_user.html', coluna = coluna)
