from flask.blueprints import Blueprint
from flask import request, session, Response, render_template, redirect, url_for, flash
from app.models.task import TaskRepository
from app.services.task_service import Tarefas
from app.models.user import UserRepository
from app.decorators import login_necessario

tarefa_bp = Blueprint('tarefa', __name__, url_prefix='/tarefa')
banco_user = UserRepository()
servico_tarefa = Tarefas()


@tarefa_bp.route('/listar', methods=['GET'])
@login_necessario
def listar_tarefas() -> str | Response:
    id_usuario = session.get('user_id')
    if id_usuario:
        tarefas = servico_tarefa.listar_tarefas(id_usuario)
        return render_template('tarefas_user.html', tarefas = tarefas)
    return redirect(url_for('homepage'))


@tarefa_bp.route('/editar/deletar/<int:id_tarefa>', methods=['GET', 'POST'])
@login_necessario
def deletar_tarefa(id_tarefa) -> Response | str:
    id_usuario = session.get('user_id')
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        usuario = banco_user.find(id_usuario)
        senha_usuario = request.form.get('password')
        resposta, mensagem = servico_tarefa.deletar_tarefa(id_tarefa, id_usuario, usuario, senha_usuario)
        if resposta:
            flash(mensagem, 'sucesso')
            return redirect(url_for('tarefa.listar_tarefas'))
        flash(mensagem, 'erro')
        return redirect(url_for('tarefa.listar_tarefas'))
    return render_template('tarefas_user.html')

@tarefa_bp.route('/editar/<int:id_tarefa>/<coluna>', methods=['GET', 'POST'])
@login_necessario
def editar_tarefa(id_tarefa, coluna) -> str | Response:
    id_usuario = session.get('user_id')
    if request.method == 'POST':
        if id_usuario:
            novo_dado = request.form.get(coluna)
            resposta, mensagem = servico_tarefa.editar_tarefas(coluna, novo_dado, id_tarefa, id_usuario)
            if resposta:
                flash(mensagem, 'sucesso')
                return redirect(url_for('tarefa.listar_tarefas'))
            flash(mensagem, 'erro')
            return redirect(url_for('tarefa.editar_tarefa', id_tarefa=id_tarefa, coluna = coluna))
    return render_template('editar_desc.html', id_tarefa=id_tarefa, coluna = coluna)

@tarefa_bp.route('/criar', methods=['GET', 'POST'])
@login_necessario
def criar_tarefa() -> Response | str:
    id_usuario = session.get('user_id')
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descrição')
        resposta, mensagem = servico_tarefa.criar_tarefa(nome, descricao, id_usuario)
        if resposta:
            flash(mensagem, 'sucesso')
            return redirect(url_for('tarefa.listar_tarefas'))
        flash(mensagem, 'erro')
        return redirect(url_for('tarefa.listar_tarefas'))
    return render_template('criar_tarefa.html')
