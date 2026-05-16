from flask.blueprints import Blueprint
from app.models.task import TaskRepository

auth_bp = Blueprint('auth', __name__, url_prefix = '/task')

class Tasks():
    def __init__(self):
        self.task_db = TaskRepository()
    def list_tasks(self, user_id) -> tuple[bool, str] | tuple[bool, dict]:
        tasks = self.list_tasks(user_id)
        if tasks:
            return True, tasks
        return False, 'You dont have tasks for show'
    def edit_tasks(self, column, novo_dado, id_task, user_id) -> tuple[bool, str]:
        if column is None or novo_dado is None or id_task is None or user_id is None:
            return False, 'Nao pode haver campos em branco!'
        try:
            self.task_db.update_task(column, novo_dado, user_id, id_task)
            return True, 'Task updated successfully!'
        except ValueError:
            return False, f'Column {column} dont exist'
    def del_task(self, id_task, user_id) -> tuple[bool, str]:
        if id_task is None or user_id is None:
            return False, 'Nao pode haver campos em branco!'
        task_deletada = self.task_db.del_task(user_id, id_task)
        if task_deletada >= 1:
            return True, 'Task deleted successfully!'
        return False, 'Nao foi possivel deletar essa tarefa'
    def create_tasks(self, nome, descricao, user_id) -> tuple[bool, str]:
            if nome is None or user_id is None or descricao is None:
                return False, 'Nao pode haver campos em braco!'
            self.task_db.insert_task(nome, descricao, user_id)
            return True, 'Task created successfully'