from flask.blueprints import Blueprint
from flask import request, session, jsonify
from app.models.task import TaskRepository
from app.services.task_service import Tasks
task_bp = Blueprint('Task', __name__, url_prefix = '/task')
task_db = TaskRepository()
task = Tasks()
@task_bp.route('/View', methods = ['GET'])
def list_tasks() -> tuple[bool, str]:
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            tasks = task.list_tasks(user_id)
            if tasks:
                return jsonify(tasks), 200
            return jsonify({'Erro': 'Voce nao possui tarefas para visualizar'}), 400
        return jsonify({"Erro": "Efetue login para prosseguir!"}), 400
@task_bp.route('/EditTask', methods = ['PUT'])
def edit_tasks() -> tuple[bool, str]:
    if request.method == 'PUT':
        user_id = session.get('user_id')
        if user_id:
            dados_postman = request.get_json()
            task_id = dados_postman.get('task_id')
            for key, value in dados_postman.items():
                resposta, msg = task.edit_tasks(key, value, task_id, user_id )
                if resposta:
                    return jsonify({'Sucesso': msg}), 200
                return jsonify({'Erro': msg}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir:'}), 400
@task_bp.route('/del_task', methods = ['DELETE'])
def del_task() -> tuple[bool, str]:
    if request.method == 'DELETE':
        user_id = session.get('user_id')
        if user_id:
            dados_postman = request.get_json()
            task_id = dados_postman.get('task_id')
            resposta, msg = task.del_task(task_id, user_id)
            if resposta:
                return jsonify({'Sucesso': msg}), 200
            return jsonify({'Erro': msg}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir!'}), 400
@task_bp.route('/create_task', methods = ['POST'])
def create_tasks() -> tuple[bool, str]:
    if request.method == 'POST':
        user_id = session.get('user_id')
        if user_id:
            dados_postman = request.get_json()
            nome = dados_postman.get('nome')
            descricao = dados_postman.get('descrição')
            resposta, msg = task.create_tasks(nome, descricao, user_id)
            if resposta:
                return jsonify({'Sucesso': msg}), 200
            return jsonify({'Erro': msg}), 400
        return jsonify({'Erro': 'Efetue login para prosseguir!'}), 400