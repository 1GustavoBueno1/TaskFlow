from flask.blueprints import Blueprint

task_bp = Blueprint('Task', __name__, url_prefix = '/task')


@task_bp.route('/')
def list_tasks() -> tuple[bool, str]:
    ...
@task_bp.route('/edit_task')
def edit_tasks() -> tuple[bool, str]:
    ...
@task_bp.route('/del_task')
def del_task() -> tuple[bool, str]:
    ...
@task_bp.route('/create_task')
def create_tasks() -> tuple[bool, str]:
    ...