from flask.blueprints import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix = 'auth')

@auth_bp.route('/register')
def register_user() -> tuple[bool, str]:
    ...
@auth_bp.route('/login')
def login() -> tuple[bool, str]:
    ...
