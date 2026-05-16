from flask.blueprints import Blueprint
from flask import request, session, jsonify, Response
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
            sucesso, tarefas = servico_tarefa.listar_tarefas(id_usuario)
            if sucesso:
                return jsonify(tarefas), 200
            return jsonify({'Erro': tarefas}), 400
        return jsonify({"Erro": "Efetue login para prosseguir!"}), 401


@tarefa_bp.route('/editar', methods=['PUT'])
def editar_tarefas() -> tuple[Response, int]:
    if request.method == 'PUT':
        id_usuario = session.get('user_id')
        if id_usuario:
            dados = request.get_json()
            id_tarefa = dados.get('id_tarefa')
            for chave, valor in dados.items():
                if chave == 'id_tarefa':
                    continue
                resposta, mensagem = servico_tarefa.editar_tarefas(chave, valor, id_tarefa, id_usuario)
                if resposta:
                    return jsonify({'Sucesso': mensagem}), 200
                return jsonify({'Erro': mensagem}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir!'}), 401


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


@tarefa_bp.route('/criar', methods=['POST'])
def criar_tarefa() -> tuple[Response, int]:
    if request.method == 'POST':
        id_usuario = session.get('user_id')
        if id_usuario:
            dados = request.get_json()
            nome = dados.get('nome')
            descricao = dados.get('descricao')
            resposta, mensagem = servico_tarefa.criar_tarefa(nome, descricao, id_usuario)
            if resposta:
                return jsonify({'Sucesso': mensagem}), 201
            return jsonify({'Erro': mensagem}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir!'}), 401
