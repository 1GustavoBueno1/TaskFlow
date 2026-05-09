from flask.blueprints import Blueprint

task_bp = Blueprint('Task', __name__, url_prefix = '/task')


@task_bp.route('/', methods = ['GET'])
def list_tasks() -> tuple[bool, str]:
    ...
@task_bp.route('/edit_task', methods = ['GET', 'PUT'])
def edit_tasks() -> tuple[bool, str]:
    ...
@task_bp.route('/del_task', methods = ['GET', 'DEL'])
def del_task() -> tuple[bool, str]:
    ...
@task_bp.route('/create_task', methods = ['GET', 'POST'])
def create_tasks() -> tuple[bool, str]:
    ...