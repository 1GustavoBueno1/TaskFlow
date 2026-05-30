from flask.blueprints import Blueprint
from flask import request, session, Response, render_template, redirect, url_for, flash
from app.models.task import TaskRepository
from app.services.task_service import Tarefas
from app.services.user_service import UserRepository


tarefa_bp = Blueprint('tarefa', __name__, url_prefix='/tarefa')
banco_tarefa = TaskRepository()
banco_user = UserRepository()
servico_tarefa = Tarefas()


@tarefa_bp.route('/listar', methods=['GET'])
def listar_tarefas() -> tuple[Response, int]:
    if request.method == 'GET':
        id_usuario = session.get('user_id')
        if id_usuario:
            tarefas = servico_tarefa.listar_tarefas(id_usuario)
            return render_template('tarefas_user.html', tarefas = tarefas)
        return redirect(url_for('homepage'))


@tarefa_bp.route('/editar/deletar/<int:id_tarefa>', methods=['GET', 'POST'])
def deletar_tarefa(id_tarefa) -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            usuario = banco_user.find(id_usuario)
            senha_usuario = request.form.get('password')
            resposta, mensagem = servico_tarefa.deletar_tarefa(id_tarefa, id_usuario, usuario, senha_usuario)
            if resposta:
                flash(mensagem, 'sucesso')
                return redirect(url_for('tarefa.listar_tarefas'))
            flash(mensagem, 'erro')
            return redirect(url_for('tarefa.listar_tarefas'))
        flash("Efetue login para prosseguir", "erro")
        return redirect(url_for('homepage'))
    return render_template('tarefas_user.html')

@tarefa_bp.route('/editar/<int:id_tarefa>/<coluna>', methods=['GET', 'POST'])
def editar_tarefa(id_tarefa, coluna) -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            novo_dado = request.form.get(coluna)
            resposta, mensagem = servico_tarefa.editar_tarefas(coluna, novo_dado, id_tarefa, id_usuario)
            if resposta:
                flash(mensagem, 'sucesso')
                return redirect(url_for('tarefa.listar_tarefas'))
            flash(mensagem, 'erro')
            return redirect(url_for('tarefa.editar_tarefa', id_tarefa=id_tarefa, coluna = coluna))
        flash("Efetue login para prosseguir", 'erro')
        return redirect(url_for('homepage'))
    return render_template('editar_desc.html', id_tarefa=id_tarefa, coluna = coluna)

@tarefa_bp.route('/criar', methods=['GET', 'POST'])
def criar_tarefa() -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            nome = request.form.get('nome')
            descricao = request.form.get('descrição')
            resposta, mensagem = servico_tarefa.criar_tarefa(nome, descricao, id_usuario)
            if resposta:
                tarefas = servico_tarefa.listar_tarefas(id_usuario)
                flash(mensagem, 'sucesso')
                return redirect(url_for('tarefa.listar_tarefas'))
            flash(mensagem, 'erro')
            return redirect(url_for('tarefa.listar_tarefas'))
        flash("Efetue login para continuar", 'erro')
        return redirect(url_for('homepage'))
    return render_template('criar_tarefa.html')
