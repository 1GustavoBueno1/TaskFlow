from flask.blueprints import Blueprint
from flask import request, session, jsonify, Response, render_template, redirect, url_for, flash
from app.models.task import TaskRepository
from app.services.task_service import Tarefas

tarefa_bp = Blueprint('tarefa', __name__, url_prefix='/tarefa')
banco_tarefa = TaskRepository()
servico_tarefa = Tarefas()


@tarefa_bp.route('/listar', methods=['GET'])
def listar_tarefas() -> tuple[Response, int]:
    if request.method == 'GET':
        id_usuario = session.get('user_id')
        if id_usuario:
            tarefas = servico_tarefa.listar_tarefas(id_usuario)
            return render_template('tarefas_user.html', tarefas = tarefas)
        return render_template('homepage')


# @tarefa_bp.route('/editar', methods=['PUT'])
# def editar_nome_da_tarefa() -> tuple[Response, int]:
#     if request.method == 'PUT':
#         id_usuario = session.get('user_id')
#         if id_usuario:
#             dados = request.get_json()
#             id_tarefa = dados.get('id_tarefa')
#             for chave, valor in dados.items():
#                 if chave == 'id_tarefa':
#                     continue
#                 resposta, mensagem = servico_tarefa.editar_tarefas(chave, valor, id_tarefa, id_usuario)
#                 if resposta:
#                     return jsonify({'Sucesso': mensagem}), 200
#                 return jsonify({'Erro': mensagem}), 400
#         return jsonify({'Erro': 'Efetue login para prosseguir!'}), 401

@tarefa_bp.route('/editar/desc/<int:id_tarefa>', methods=['GET', 'POST'])
def editar_desc_da_tarefa(id_tarefa) -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            desc = request.form.get('descrição')
            resposta, mensagem = servico_tarefa.editar_tarefas('description', desc, id_tarefa, id_usuario)
            if resposta:
                flash(mensagem, 'sucesso')
                return redirect(url_for('tarefa.listar_tarefas')), 200
            flash(mensagem, 'erro'), 400
            return redirect(url_for('tarefa.editar_desc_da_tarefa', id_tarefa=id_tarefa)), 400
        flash("Efetue login para prosseguir", 'erro')
        return redirect(url_for('homepage')), 401
    return render_template('editar_desc.html', id_tarefa=id_tarefa)

# @tarefa_bp.route('/editar', methods=['PUT'])
# def alterar_status_da_tarefa() -> tuple[Response, int]:
#     if request.method == 'PUT':
#         id_usuario = session.get('user_id')
#         if id_usuario:
#             dados = request.get_json()
#             id_tarefa = dados.get('id_tarefa')
#             for chave, valor in dados.items():
#                 if chave == 'id_tarefa':
#                     continue
#                 resposta, mensagem = servico_tarefa.editar_tarefas(chave, valor, id_tarefa, id_usuario)
#                 if resposta:
#                     return jsonify({'Sucesso': mensagem}), 200
#                 return jsonify({'Erro': mensagem}), 400
#         return jsonify({'Erro': 'Efetue login para prosseguir!'}), 401


@tarefa_bp.route('/deletar', methods=['DELETE'])
def deletar_tarefa() -> tuple[Response, int]:
    if request.method == 'DELETE':
        id_usuario = session.get('user_id')
        if id_usuario:
            dados = request.get_json()
            id_tarefa = dados.get('id_tarefa')
            resposta, mensagem = servico_tarefa.deletar_tarefa(id_tarefa, id_usuario)
            if resposta:
                return jsonify({'Sucesso': mensagem}), 200
            return jsonify({'Erro': mensagem}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir!'}), 401


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
                flash(mensagem, 'sucesso'), 201
                return redirect(url_for('tarefa.listar_tarefas')), 201
            flash(mensagem, 'erro')
            return redirect(url_for('tarefa.listar_tarefas')), 400
        flash("Efetue login para continuar", 'erro'), 400
        return redirect(url_for('homepage')), 401
    return render_template('criar_tarefa.html')
