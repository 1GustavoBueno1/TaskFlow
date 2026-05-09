from flask.blueprints import Blueprint

user_bp = Blueprint('/user', __name__, url_prefix = '/profile')

@user_bp.route('/', methods = ['GET'])
def view_profile(self) -> tuple[bool, str]:
    ...
@user_bp.route('/Edit_User_Profile', methods = ['GET', 'PUT'])
def edit_profile(self) -> tuple[bool, str]:
    ...