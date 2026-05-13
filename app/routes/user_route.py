from flask.blueprints import Blueprint
from flask import request, jsonify, session
from app.models.user import UserRepository
user_bp = Blueprint('user', __name__, url_prefix = '/profile')
user_db = UserRepository()
@user_bp.route('/view', methods = ['GET'])
def view_profile() -> tuple[bool, str]:
    if request.method == 'GET':
        user_id = session.get('user_id')
        user = user_db.find(user_id)
        if user_id:
            return jsonify({"Nome": user['name'], 
                            "email": user['gmail']})
        return jsonify({"Erro": 'Efetue login para continuar!'})
@user_bp.route('/Edit_User_Profile', methods = ['GET', 'PUT'])
def edit_profile() -> tuple[bool, str]:
    if request.method == 'PUT':
        ...