from flask.blueprints import Blueprint

user_bp = Blueprint('user', __name__, url_prefix = 'profile')

@user_bp.route('/')
def view_profile(self) -> tuple[bool, str]:
    ...
@user_bp.route
def edit_profile(self) -> tuple[bool, str]:
    ...