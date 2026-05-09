from flask.blueprints import Blueprint
from flask import request

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_bp.route('/register', methods = ['GET', 'POST'])
def register_user() -> tuple[bool, str]:
    ...
@auth_bp.route('/login', methods = ['GET', 'POST'])
def login() -> tuple[bool, str]:
    if request.method
